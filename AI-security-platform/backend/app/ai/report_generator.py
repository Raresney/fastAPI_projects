import json
from openai import AsyncOpenAI
from app.config import get_settings
from app.models.report import ReportType

settings = get_settings()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

EXECUTIVE_PROMPT = """You are a cybersecurity analyst writing an executive summary report.
Given the following vulnerability scan findings for target: {target_url}

Findings:
{findings_text}

Generate a JSON report with:
- "risk_score": overall risk score 1-100
- "risk_level": "critical", "high", "medium", or "low"
- "executive_summary": 2-3 paragraph non-technical summary for executives
- "key_risks": list of top 3-5 risks with business impact
- "recommendations": prioritized list of 3-5 actionable recommendations
- "compliance_notes": any relevant compliance implications (OWASP, PCI-DSS, etc.)

Return ONLY valid JSON."""

TECHNICAL_PROMPT = """You are a senior penetration tester writing a technical vulnerability report.
Given the following vulnerability scan findings for target: {target_url}

Findings:
{findings_text}

Generate a JSON report with:
- "target": the scanned target
- "total_findings": count of findings by severity
- "vulnerability_details": for each finding, provide:
  - "title": finding title
  - "severity": severity level
  - "cvss_estimate": estimated CVSS score
  - "technical_description": detailed technical explanation
  - "proof_of_concept": how to verify/reproduce
  - "remediation_steps": step-by-step fix instructions
  - "references": relevant CWE/OWASP references
- "attack_surface_analysis": overall attack surface assessment
- "remediation_roadmap": prioritized fix timeline

Return ONLY valid JSON."""


def _format_findings(findings) -> str:
    lines = []
    for f in findings:
        lines.append(f"- [{f.severity.value.upper()}] {f.title}: {f.description}")
        if f.evidence:
            lines.append(f"  Evidence: {f.evidence[:200]}")
    return "\n".join(lines)


async def generate_ai_report(target_url: str, findings: list, report_type: ReportType) -> dict:
    if not client:
        return _generate_fallback(target_url, findings, report_type)

    findings_text = _format_findings(findings)
    prompt = EXECUTIVE_PROMPT if report_type == ReportType.EXECUTIVE else TECHNICAL_PROMPT
    prompt = prompt.format(target_url=target_url, findings_text=findings_text)

    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=3000,
        )
        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]

        parsed = json.loads(content)
        summary = parsed.get("executive_summary", parsed.get("attack_surface_analysis", ""))

        return {"content": parsed, "summary": summary}
    except Exception:
        return _generate_fallback(target_url, findings, report_type)


def _generate_fallback(target_url: str, findings: list, report_type: ReportType) -> dict:
    severity_counts = {}
    for f in findings:
        sev = f.severity.value
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    critical = severity_counts.get("critical", 0)
    high = severity_counts.get("high", 0)

    if critical > 0:
        risk_level = "critical"
        risk_score = 90
    elif high > 0:
        risk_level = "high"
        risk_score = 70
    else:
        risk_level = "medium"
        risk_score = 45

    content = {
        "target": target_url,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "total_findings": severity_counts,
        "findings": [
            {
                "title": f.title,
                "severity": f.severity.value,
                "description": f.description,
                "remediation": f.remediation,
            }
            for f in findings
        ],
    }

    summary = (
        f"Security scan of {target_url} identified {len(findings)} finding(s). "
        f"Risk level: {risk_level.upper()} (score: {risk_score}/100). "
        f"Breakdown: {', '.join(f'{v} {k}' for k, v in severity_counts.items())}."
    )

    return {"content": content, "summary": summary}
