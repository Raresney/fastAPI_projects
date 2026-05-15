from app.services.scan_modules.headers import SecurityHeadersModule
from app.services.scan_modules.cors import CORSModule
from app.services.scan_modules.cookies import CookieSecurityModule
from app.services.scan_modules.methods import HTTPMethodsModule
from app.services.scan_modules.robots import RobotsModule
from app.services.scan_modules.redirects import OpenRedirectModule
from app.services.scan_modules.directory_listing import DirectoryListingModule
from app.services.scan_modules.rate_limiting import RateLimitingModule

ALL_MODULES = [
    SecurityHeadersModule,
    CORSModule,
    CookieSecurityModule,
    HTTPMethodsModule,
    RobotsModule,
    OpenRedirectModule,
    DirectoryListingModule,
    RateLimitingModule,
]
