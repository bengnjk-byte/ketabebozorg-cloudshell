KETABEBOZORG official program ladder 2026-09-10
Authority: CE-C0 binding OIDC text + Rung 3 gate table.
Book lane separate. REV7 READ_ONLY. I9/Q10 HOLD.

1 DONE Drive Lite
2A DONE Frozen ZIP on Drive
     SHA-256 daede0951db98e8442bb44e43eae64c1bf1e237082dec7cd51140129b05b87f2
     76877 bytes. Drive 1oe7AE_PD0WvbcMh8qUjS9YbWRUj7qwlk
2B DONE Exact bytes → runner via V6.zip.b64
     DO NOT REOPEN

## Activation gate
Cloud stays off until Rung 3 closes.
This chat has no control-plane access to GCP, so it cannot create
pool/provider or IAM binding. It will not dispatch GitHub while
WIF_PROVIDER is UNSET (that run is designed to fail-close).

Next step, only, in an accessible Google Cloud Console / Work Cloud Browser:
  github-pool
  + github-provider
  + repository restriction on bengnjk-byte/ketabebozorg-cloudshell
  + roles/iam.workloadIdentityUser
  + set WIF_PROVIDER (full resource name, numeric project number)

After RUNG 3 = PASS: Cloud Run CONNECTED_READ_ONLY only.
WRITE stays OFF. Scheduler stays OFF.

GitHub OIDC capability     READY
Live OIDC token            NOT YET REQUESTED/OBSERVED
GCP WIF trust              NOT VERIFIED
WIF_PROVIDER               UNSET
Cloud Run                  NOT STARTED

## Rung 3 gate table

| مؤلفه | وضعیت فعلی | شواهد / توضیح | شرط PASS |
|---|---|---|---|
| GitHub OIDC permission | READY | `id-token: write` در workflow موجود است | بدون تغییر |
| GitHub OIDC token | NOT YET OBSERVED | فقط هنگام جریان واقعی job درخواست می‌شود | controlled run توکن را با موفقیت درخواست کند |
| Repository identity | KNOWN | `bengnjk-byte/ketabebozorg-cloudshell` | provider دقیقاً همین repo را بپذیرد |
| WIF pool `github-pool` | UNKNOWN | هنوز GCP live-read نداریم | وجود + enabled بودن تأیید شود |
| WIF provider `github-provider` | UNKNOWN | هنوز GCP live-read نداریم | وجود + enabled بودن تأیید شود |
| OIDC issuer | UNKNOWN IN GCP | باید GitHub issuer باشد | `https://token.actions.githubusercontent.com/` تأیید شود |
| Attribute mapping | UNKNOWN | هنوز mapping دیده نشده | repository و claimهای لازم درست map شوند |
| Repository restriction | UNKNOWN | هنوز GCP trust دیده نشده | فقط `bengnjk-byte/ketabebozorg-cloudshell` مجاز باشد |
| Provider condition | UNKNOWN | ممکن است absent یا نادرست باشد | شرط repository-scoped معتبر باشد |
| Service account | UNKNOWN | فقط نام هدف در workflow داریم | `ketabebozorg-runner@ketabebozorg-orchestrator.iam.gserviceaccount.com` وجود و enabled بودنش تأیید شود |
| `roles/iam.workloadIdentityUser` | UNKNOWN | binding هنوز دیده نشده | روی service account برای principal مناسب برقرار باشد |
| GitHub variable `WIF_PROVIDER` | UNSET | confirmed blocker | full provider resource name با numeric project number تنظیم شود |
| GCP project access | BLOCKED/UNKNOWN | Work Cloud Browser به Console نرسید | پروژه `ketabebozorg-orchestrator` live باز و قابل بازرسی باشد |
| GCP trust chain | NOT VERIFIED | GitHub آماده است ولی Google-side trust اثبات نشده | STS token exchange + SA impersonation موفق شود |
| Rung 3 overall | OPEN | دو blocker قطعی: Cloud access و `WIF_PROVIDER` unset | تمام ردیف‌های الزامی PASS + controlled auth test موفق |
| Rung 4 Cloud Run | WAITING | نباید قبل از Rung 3 شروع شود | فقط پس از RUNG 3 = PASS |
| WRITE | OFF | fail-closed | همچنان OFF بماند |
| Scheduler | OFF | fail-closed | همچنان OFF بماند |
| 2B | DONE / CLOSED | frozen delivery path کامل است | DO NOT REOPEN |

Do not Run deploy-readonly until WIF_PROVIDER is proven.
Do not invent SERVICE_URL.
Do not open WRITE, Scheduler, I9, or Q10.
Do not reopen 2B.
