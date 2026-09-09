KETABEBOZORG official program ladder 2026-09-10
Authority: CE-C0 corrected activation procedure.
Book lane separate. REV7 READ_ONLY. I9/Q10 HOLD.

1 DONE Drive Lite
2A DONE Frozen ZIP on Drive
     SHA-256 daede0951db98e8442bb44e43eae64c1bf1e237082dec7cd51140129b05b87f2
2B DONE Exact bytes → runner via V6.zip.b64 — DO NOT REOPEN

GitHub OIDC capability     READY
Live OIDC token            NOT YET REQUESTED/OBSERVED
GCP WIF trust              NOT VERIFIED
WIF_PROVIDER               UNSET
Rung 3                     OPEN
Rung 3 CONFIGURED          NO
Rung 3 PASS                NO — requires live OIDC→STS→impersonation
Rung 4                     WAITING — Cloud Run/source/Build/AR are Rung 4
WRITE OFF
Scheduler OFF

## Activation gate (corrected)
This chat cannot create GCP WIF or IAM.
Do not dispatch while WIF_PROVIDER is UNSET.
Do not retry the blocked Cloud Browser path as a substitute for a reachable console.
Keep auth@v2 until live evidence says otherwise.

TWO LAYERS, both required:
  Provider admission condition
    → only bengnjk-byte/ketabebozorg-cloudshell admitted
  AND service-account IAM binding
    → roles/iam.workloadIdentityUser for that repository principalSet only

PASS is not CONFIGURED. Setting pool/provider/WIF_PROVIDER = CONFIGURED.
PASS = controlled run with allow_rung4=false proves:
  Frozen ZIP gate PASS
  GitHub OIDC request PASS
  Google STS exchange PASS
  Provider condition PASS
  Repository restriction PASS
  SA impersonation PASS
Then Rung 4 may start.

Safer sequence: see GCP_WIF_ONE_TIME_THEN_ACTIONS.md steps 1–16.

## Rung 3 gate table

| مؤلفه | وضعیت فعلی | شواهد / توضیح | شرط PASS |
|---|---|---|---|
| GitHub OIDC permission | READY | `id-token: write` موجود است | بدون تغییر |
| GitHub OIDC token | NOT YET OBSERVED | فقط هنگام job واقعی | controlled run توکن را درخواست کند |
| Repository identity | KNOWN | `bengnjk-byte/ketabebozorg-cloudshell` | provider همین repo را بپذیرد |
| Account IAM authority | UNKNOWN | باز کردن پروژه کفایت نیست | حساب بتواند WIF و SA IAM بسازد |
| IAM + STS + IAM Credentials APIs | UNKNOWN | قبل از قابل-استفاده دانستن provider | enabled تأیید شوند |
| WIF pool `github-pool` | UNKNOWN | بدون GCP live-read | وجود + enabled |
| WIF provider `github-provider` | UNKNOWN | بدون GCP live-read | وجود + enabled |
| OIDC issuer | UNKNOWN IN GCP | باید GitHub issuer باشد | `https://token.actions.githubusercontent.com/` |
| Attribute mapping | UNKNOWN | باید `sub` + `repository` | mapping درست |
| Provider admission condition | UNKNOWN | دو لایه الزامی است؛ IAM تنها کافی نیست | `assertion.repository == 'bengnjk-byte/ketabebozorg-cloudshell'` |
| Repository IAM principalSet | UNKNOWN | لایه دوم | `workloadIdentityUser` فقط برای همین repo |
| Service account | UNKNOWN | فقط نام هدف در YAML | وجود + enabled قبل از bind |
| `WIF_PROVIDER` | UNSET | confirmed blocker؛ project NUMBER | full resource name تنظیم شود |
| GitHub variable write | MAY BE MANUAL | این چت شاید نتواند variable بنویسد | مقدار در Actions variables دیده شود |
| GCP project access | BLOCKED/UNKNOWN | Cloud Browser به Console نرسید | پروژه live قابلبازرسی |
| GCP trust chain | NOT VERIFIED | GitHub آماده؛ Google اثبات‌نشده | STS + impersonation زنده |
| Rung 3 CONFIGURED | NO | pool/provider/variable بدون job زنده | تنظیمات بازخوانی شد |
| Rung 3 PASS | NO | تنظیم کافی نیست | همه ردیف‌های الزامی + auth test موفق |
| Rung 4 Cloud Run | WAITING | Build/AR/IAM جدا؛ با WIF قاطی نشود | فقط پس از RUNG 3 PASS |
| Private /health | NOT STARTED | براوز عادی کافی نیست | authenticated invocation |
| Drive read | NOT STARTED | موفقیت Cloud Run دلیل Drive نیست | گیت جدا |
| WRITE | OFF | fail-closed | OFF بماند |
| Scheduler | OFF | fail-closed | OFF بماند |
| 2B | DONE / CLOSED | frozen path کامل | DO NOT REOPEN |

Do not Run until WIF_PROVIDER is proven.
Do not invent SERVICE_URL.
Do not open WRITE, Scheduler, I9, or Q10.
Do not reopen 2B.
