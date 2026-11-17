# Cài BA Skills Kit cho Claude Code, Codex và Antigravity

Tài liệu này hướng dẫn cài 9 skill pipeline và 2 skill phụ `ba-explore-project`, `ba-pbi` (tổng 11 skill) vào công cụ AI bạn sử dụng, tạo cấu hình dự án và chạy lần đầu. Giới thiệu/thuật ngữ ở [README.md](README.md); quy trình cùng các file đầu ra ở [hướng dẫn project hiện có](GUIDE_EXISTING_PROJECT.md) và [hướng dẫn project mới](GUIDE_NEW_PROJECT.md).

**Chọn một công cụ, làm phần chuẩn bị chung, cài theo hướng dẫn riêng, rồi tạo cấu hình và bắt đầu.** Không cần cài cả ba.

## 1. Chọn nơi cài

Khuyến nghị người mới **cài theo project**: skill chỉ nằm trong thư mục dự án bạn muốn phân tích. Cài cá nhân dùng chung nhiều project là lựa chọn thêm ở cuối tài liệu.

| Công cụ | Thư mục skill trong project | Cách bắt đầu |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `/ba-workflow` trong chat Claude Code |
| Codex | `.agents/skills/` | `$ba-workflow` hoặc chọn skill trong giao diện |
| Antigravity | `.agents/skills/` | Nêu tên `ba-workflow` trong yêu cầu; xem hướng dẫn riêng bên dưới |

Đường dẫn và cách gọi được đối chiếu theo [Claude Code Skills](https://code.claude.com/docs/en/skills), [Codex Build skills](https://learn.chatgpt.com/docs/build-skills) và [Antigravity Agent skills](https://antigravity.google/docs/skills), ngày 17/11/2026.

Trong tài liệu này, **Claude là Claude Code chạy với thư mục local**, bao gồm terminal hoặc giao diện tích hợp Claude Code. Cài bằng cách upload ZIP lên Claude web/Cowork là luồng phân phối khác; các lệnh local bên dưới dành cho Claude Code.

## 2. Chuẩn bị chung — làm một lần

### Bạn cần có

- Công cụ đã cài và đăng nhập: Claude Code, Codex hoặc Antigravity.
- Python 3.10 trở lên.
- Bộ BA Skills Kit đã giải nén, có các thư mục `skills/`, `scripts/`, `contracts/` và file `requirements-kit.txt`.
- Một thư mục dự án đích. Có thể dùng project mới, chưa có mã nguồn.

Ví dụ xuyên suốt tài liệu:

| Đường dẫn ví dụ | Dùng để làm gì? |
| --- | --- |
| `D:\BA-Skills-Kit` | Giữ Kit nguồn và môi trường Python |
| `D:\Projects\MyProject` | Project cần phân tích; thay bằng đường dẫn thật |

**Lệnh trong khối `powershell` hoặc `bash` chạy ở terminal. Khối `text` gửi vào chat của công cụ AI.**

### Windows / PowerShell

Mở PowerShell, vào Kit và cài thư viện:

```powershell
cd "D:\BA-Skills-Kit"
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-kit.txt
```

`python --version` phải hiển thị từ 3.10 trở lên. Nếu lệnh chưa được nhận diện, cài Python và mở lại terminal. Lần cài thư viện cần kết nối tới nguồn gói Python của môi trường bạn dùng.

Nếu chưa có thư mục dự án, tạo trước:

```powershell
New-Item -ItemType Directory -Force -Path "D:\Projects\MyProject"
```

### macOS / Linux

Thay đường dẫn bằng vị trí Kit và project trên máy:

```bash
cd "$HOME/BA-Skills-Kit"
python3 --version
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-kit.txt
mkdir -p "$HOME/Projects/MyProject"
```

Các lệnh cài riêng dưới đây dùng ví dụ Windows. Trên macOS/Linux, thay `.\.venv\Scripts\python.exe` bằng `./.venv/bin/python` và thay đường dẫn project tương ứng.

## 3A. Cài cho Claude Code

Từ terminal tại thư mục Kit, chạy xem trước:

```powershell
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "D:\Projects\MyProject\.claude\skills"
```

Kiểm tra đường dẫn đúng project, sau đó cài:

```powershell
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "D:\Projects\MyProject\.claude\skills" --apply
```

Theo [tài liệu Claude Code](https://code.claude.com/docs/en/skills#choose-where-skills-load), skill local của project nằm trong `.claude/skills`. Ví dụ sau cài đặt:

```text
MyProject/.claude/skills/ba-workflow/SKILL.md
MyProject/.claude/skills/ba-spec/SKILL.md
... cùng 9 skill còn lại
```

Mở Claude Code tại project. Nếu dùng CLI đã cài, chạy ở terminal:

```powershell
cd "D:\Projects\MyProject"
claude
```

Sau khi tạo cấu hình theo mục 4, gửi trong chat Claude Code:

```text
/ba-workflow mode=INTERACTIVE project_config=./.temp/ba-project.yaml

Tôi muốn website ghi chú cá nhân và công ty, tạo tài liệu từ mẫu và tìm kiếm.
Hãy bắt đầu từ brainstorm, dừng để tôi duyệt backlog, Round và trước publish.
Dùng Python D:/BA-Skills-Kit/.venv/Scripts/python.exe để chạy công cụ Kit.
```

Kiểm tra `/ba-workflow` trong danh sách lệnh `/`. Nếu chưa thấy, mở phiên mới tại đúng project. Trong thân các SKILL.md nguồn có ví dụ `$ba-…` theo Codex; khi gọi skill trên Claude Code, dùng `/ba-…`, còn các tham số giữ cùng ý nghĩa.

## 3B. Cài cho Codex

Từ terminal tại thư mục Kit, chạy xem trước:

```powershell
.\.venv\Scripts\python.exe scripts/install_skills.py --project-root "D:\Projects\MyProject"
```

Sau đó cài:

```powershell
.\.venv\Scripts\python.exe scripts/install_skills.py --project-root "D:\Projects\MyProject" --apply
```

`--project-root` của installer mặc định cài vào `.agents/skills`, phù hợp với [vị trí discovery của Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

Mở project trong Codex hoặc IDE có Codex. Nếu dùng CLI đã cài:

```powershell
cd "D:\Projects\MyProject"
codex
```

Sau khi tạo cấu hình theo mục 4, gửi trong chat:

```text
$ba-workflow mode=INTERACTIVE project_config=./.temp/ba-project.yaml

Tôi muốn website ghi chú cá nhân và công ty, tạo tài liệu từ mẫu và tìm kiếm.
Hãy bắt đầu từ brainstorm, dừng để tôi duyệt backlog, Round và trước publish.
Dùng Python D:/BA-Skills-Kit/.venv/Scripts/python.exe để chạy công cụ Kit.
```

CLI/IDE hỗ trợ chọn skill bằng `$` hoặc `/skills`; giao diện khác có thể có menu chọn skill. Nếu chưa thấy `ba-workflow`, mở phiên mới hoặc khởi động lại Codex.

## 3C. Cài cho Antigravity

Từ terminal tại thư mục Kit, chạy xem trước:

```powershell
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "D:\Projects\MyProject\.agents\skills"
```

Sau đó cài:

```powershell
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "D:\Projects\MyProject\.agents\skills" --apply
```

[Tài liệu Antigravity hiện tại](https://antigravity.google/docs/skills#skills-by-surface) dùng `.agents/skills` cho workspace; `.agent/skills` là đường dẫn tương thích cũ. Dùng đường dẫn hiện tại cho bản cài mới.

Mở `D:\Projects\MyProject` trong Antigravity. Với IDE, xem skill đang hoạt động tại **Customizations** trong agent side panel. Sau khi tạo cấu hình theo mục 4, gửi:

```text
Hãy dùng skill ba-workflow trong workspace này.
mode=INTERACTIVE project_config=./.temp/ba-project.yaml

Tôi muốn website ghi chú cá nhân và công ty, tạo tài liệu từ mẫu và tìm kiếm.
Hãy bắt đầu từ brainstorm, dừng để tôi duyệt backlog, Round và trước publish.
Dùng Python D:/BA-Skills-Kit/.venv/Scripts/python.exe để chạy công cụ Kit.
```

Antigravity App/CLI cũng hỗ trợ `/ba-workflow`; CLI có `/skills reload` để nạp skill mới. Với IDE, nếu chưa nhận diện được, mở phiên mới và kiểm tra Customizations. Không cần tạo thêm workflow slash-command riêng cho bộ skill này.

## 4. Tạo cấu hình dự án — áp dụng cho cả ba

Với project chưa có cấu hình BA, tạo `.temp` rồi copy mẫu từ Kit vào đó. Nếu đã có `ba-project.yaml` ở root hoặc trong `.temp`, kiểm tra bản hiện tại; xem phần chuyển cấu hình cũ bên dưới, không tạo thêm bản mới hay ghi đè.

Windows:

```powershell
New-Item -ItemType Directory -Force -Path "D:\Projects\MyProject\.temp"
Copy-Item -LiteralPath ".\templates\ba-project.example.yaml" -Destination "D:\Projects\MyProject\.temp\ba-project.yaml"
```

macOS/Linux:

```bash
mkdir -p "$HOME/Projects/MyProject/.temp"
cp -n templates/ba-project.example.yaml "$HOME/Projects/MyProject/.temp/ba-project.yaml"
```

Mở file, sửa ít nhất mã và tên dự án:

```yaml
config_version: '1.0'
project_id: my-notes
project_name: My Notes
repository_root: .
output_root: .specify
planning_dir: .temp
round_prefix: R
pbi_prefix: PBI
language: vi
skill_runtime: codex
approval_policy: human_checkpoints
```

| Trường | Cách điền |
| --- | --- |
| `project_id` | Mã riêng: chữ thường không dấu, có thể dùng `-`, ví dụ `my-notes` |
| `project_name` | Tên sản phẩm hiển thị |
| `repository_root` | Giữ `.`; với config trong `.temp`, đây vẫn là root project chứa `.temp` |
| `output_root` | Giữ `.specify` nếu muốn dùng vị trí mặc định |
| `planning_dir` | Giữ `.temp`; chứa phân tích, nháp, review và tiến độ |
| `round_prefix` / `pbi_prefix` | Giữ `R` / `PBI` khi mới dùng |
| `language` | `vi` để nội dung tiếng Việt |
| `skill_runtime` | **Giữ `codex` trên cả ba công cụ trong phiên bản Kit hiện tại**, xem giải thích dưới |
| Các trường còn lại | Giữ như mẫu |

**Giới hạn tương thích cấu hình:** schema hiện chỉ chấp nhận `skill_runtime: codex`. Trường này chưa được các helper dùng để chọn công cụ thực thi; nơi cài skill và công cụ bạn mở mới quyết định agent nào chạy. Đổi thành `claude` hoặc `antigravity` sẽ gây `INVALID_CONFIG`. Hướng dẫn này dùng khả năng cài vào thư mục tùy chọn của installer, chưa mở rộng enum của schema.

Các đường dẫn được resolve từ root project, không từ nơi cài skill hay nơi giữ Kit nguồn. Với ví dụ này, chỉ cặp tài liệu publish nằm dưới `D:\Projects\MyProject\.specify`; hồ sơ trung gian nằm trong `.temp`.

Các helper tự tìm `.temp/ba-project.yaml` khi chạy tại root project; không cần truyền `project_config` trong mọi câu nhắn. File `ba-project.yaml` cũ ở root vẫn đọc được khi chưa có bản trong `.temp`. Nếu cả hai tồn tại thì bản trong `.temp` được ưu tiên; nếu bản đó có lỗi, helper báo lỗi để sửa.

**Chuyển riêng file cấu hình cũ:** cập nhật skill theo mục 8, rồi chuyển `ba-project.yaml` từ root vào `.temp/ba-project.yaml` nếu chưa có file ở đích. Giữ `repository_root: .`, `planning_dir: .temp`, `output_root: .specify`. Không cần chuyển hay tạo lại tài liệu PBI. Kiểm tra bằng lệnh audit bên dưới; nếu config cũng được dùng làm nguồn có hash, kiểm lại nguồn đó theo [quy ước cấu hình](conventions/BA-CONVENTIONS.md#kit-root-project-root-và-an-toàn-đường-dẫn).

**Phân vùng bắt buộc:** `.specify` chỉ chứa Round/PBI-ID-slug/{business.md,spec.md}; toàn bộ hồ sơ làm việc nằm dưới `D:\Projects\MyProject\.temp`. Helper chặn planning_dir ở ngoài `.temp` hoặc output_root chồng lên `.temp`. Không xóa `.temp` sau publish vì source refs/hash và RESUME cần các file ở đó.

**Project đã dùng bản cũ:** nếu config còn `planning_dir: .specify/_planning` hoặc `_planing`, đổi đường dẫn phải đi cùng chuyển dữ liệu và sửa refs/hash có kiểm soát theo [quy trình migration](conventions/BA-CONVENTIONS.md#chuyển-dự-án-đang-dùng-layout-cũ). Installer chỉ cập nhật skills, không tự di chuyển hồ sơ dự án. Có thể yêu cầu agent: “Chuyển hồ sơ BA trung gian từ layout cũ sang .temp, giữ các cặp Round/PBI, kiểm conflicts và refs/hash, không xóa dữ liệu; báo review/approval cần xác nhận lại.”

Kiểm cấu trúc sau khi chuyển:

```powershell
.\.venv\Scripts\python.exe scripts/check_ba_layout.py --project-config "D:/Projects/MyProject/.temp/ba-project.yaml" --check-documents
```

## 5. Kiểm tra đã cài thành công

### File hướng dẫn chung và discovery skill

Trong **Kit nguồn**, [AGENTS.md](AGENTS.md) là chỉ dẫn workspace, [SKILL.md](SKILL.md) là bộ chỉ đường, [CLAUDE.md](CLAUDE.md) import AGENTS.md. Tên file chuẩn cho Codex là **AGENTS.md**, không phải AGENT.md. Tham khảo [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code project instructions](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools) và [Antigravity rules](https://antigravity.google/docs/rules): Antigravity hiện cũng đọc AGENTS.md ở workspace.

Installer cài các skill trong `skills/` và tài nguyên riêng (hiện có 11 skill), không ghi đè AGENTS.md/CLAUDE.md hay cấu hình chỉ dẫn của project đích. Mỗi skill có SKILL.md trong thư mục discovery ở mục 1; đó là điểm vào khi gọi skill đã cài. Root SKILL.md của Kit không tự được discovery chỉ vì Kit nằm đâu đó trên máy.

Nếu không cài mà yêu cầu đọc Kit trực tiếp, chỉ định đường dẫn AGENTS.md và SKILL.md theo [ví dụ trong điểm vào cho agent](SKILL.md#khi-kit-chưa-được-cài-vào-runtime). Nếu Kit ở ngoài workspace, agent cần quyền đọc vị trí đó theo môi trường của bạn. Mở Codex trong project con không làm nó tự quét mọi Kit bên cạnh.

### Kiểm tra bản đã cài

1. Thư mục skill của công cụ có đủ 11 thư mục `ba-*`, bao gồm `ba-explore-project` và `ba-pbi`; mỗi thư mục có `SKILL.md`.
2. Ví dụ `ba-workflow/references/kit/` có `contracts/`, `conventions/`, `templates/`, `scripts/`. Installer đóng gói các tài nguyên này để skill không bị mất liên kết khi sang project khác. Chỉ copy riêng SKILL.md sẽ thiếu tài nguyên.
3. Cấu hình nằm tại `<project>/.temp/ba-project.yaml` và bạn đã xác nhận tên/đường dẫn.
4. Agent đọc được skill và chạy được Python đã cài thư viện.

Có thể thử trước khi tạo hồ sơ thật bằng lời nhắn:

```text
Hãy đọc skill ba-workflow đã cài và kiểm tra .temp/ba-project.yaml.
Dùng Python D:/BA-Skills-Kit/.venv/Scripts/python.exe để chạy công cụ Kit.
Cho biết đường dẫn planning/output đã resolve và skill nào còn thiếu.
Chưa tạo hồ sơ phân tích cho tới khi tôi gửi ý tưởng.
```

Sau đó chọn [luồng project hiện có](GUIDE_EXISTING_PROJECT.md) để bắt đầu bằng ba-explore-project, hoặc [luồng project mới](GUIDE_NEW_PROJECT.md) để bắt đầu từ ý tưởng. Hai file hướng dẫn các bước, lần duyệt và đầu ra; dùng cú pháp gọi tương ứng công cụ ở mục 3A, 3B hoặc 3C.

## 6. Tiếp tục hoặc chạy riêng một skill

| Công cụ | Ví dụ tiếp tục workflow | Ví dụ viết spec đúng một PBI |
| --- | --- | --- |
| Claude Code | `/ba-workflow mode=RESUME project_config=./.temp/ba-project.yaml` | `/ba-spec pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` |
| Codex | `$ba-workflow mode=RESUME project_config=./.temp/ba-project.yaml` | `$ba-spec pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` |
| Antigravity | “Dùng ba-workflow, mode=RESUME, project_config=./.temp/ba-project.yaml” | “Dùng ba-spec, pbi_id=PBI-001, project_config=./.temp/ba-project.yaml” |

Gửi trong chat và nhắc đường dẫn Python nếu phiên mới chưa có thông tin. Skill đơn lẻ cần đủ input hợp lệ. `ba-workflow` có thể điều phối nhiều bước khi bạn yêu cầu; review PASS vẫn cần quyết định publish của bạn.

## 7. Cài cá nhân dùng cho nhiều project — tùy chọn

Windows, từ thư mục Kit, **chọn một** lệnh theo công cụ. Chạy bỏ `--apply` trước nếu muốn xem trước.

```powershell
# Claude Code
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "$env:USERPROFILE/.claude/skills" --apply

# Codex
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "$env:USERPROFILE/.agents/skills" --apply

# Antigravity hiện tại
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "$env:USERPROFILE/.gemini/config/skills" --apply
```

macOS/Linux: dùng `./.venv/bin/python` và thay `$env:USERPROFILE` bằng `$HOME` trong đường dẫn. Mỗi project vẫn cần `.temp/ba-project.yaml` riêng. Nơi cài cá nhân được mô tả trong tài liệu chính thức liên kết ở mục 1; tránh cài trùng cùng tên ở cả phạm vi cá nhân/project khi chưa cần.

Nếu dùng Codex và Antigravity trên cùng project, có thể dùng chung bản cài `.agents/skills`. Claude Code có bản cài ở `.claude/skills`. Khi chuyển công cụ, chỉ cho một agent cập nhật cùng hồ sơ tại một thời điểm và dùng RESUME để kiểm tra nguồn.

## 8. Cập nhật bản đã cài

**BA-PBI** là skill phụ để thêm một PBI mới và tạo bộ tài liệu draft sau duyệt scope. Installer tự thêm `ba-pbi` khi cập nhật. Gọi `$ba-pbi` trong Codex hoặc `/ba-pbi` trong Claude Code, rồi mô tả tính năng; không cần sửa SKILL.md cũ. Cài theo project/global thì dùng lại thư mục đã chọn ở lần cài trước.

Bản Kit hiện có thêm **BA-explore-project** để khảo sát tính năng hiện hữu trước khi tài liệu hóa. Installer tự thêm thư mục `ba-explore-project` khi cài/cập nhật; không cần sửa chín SKILL.md cũ. Cài global hay project thì dùng lại đúng `--skills-dir` trước đây, mở phiên agent mới để thấy skill phụ. Gọi `$ba-explore-project` trong Codex hoặc `/ba-explore-project` trong Claude Code. Skill dừng ở báo cáo/brief; sau khi bạn chọn phạm vi, chuyển sang ba-workflow theo [hướng dẫn project hiện có](GUIDE_EXISTING_PROJECT.md).

Tại Kit nguồn mới, dùng **đúng thư mục đã cài trước đó**, thêm `--update`:

```powershell
# Ví dụ Claude Code; thay .claude bằng .agents cho Codex/Antigravity
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "D:\Projects\MyProject\.claude\skills" --update
.\.venv\Scripts\python.exe scripts/install_skills.py --skills-dir "D:\Projects\MyProject\.claude\skills" --update --apply
```

`create` = tạo mới; `update` = cập nhật file do installer quản lý; `skip` = nội dung đã giống nhau. `INSTALL_CONFLICT` = có chỉnh sửa local hoặc file ngoài quản lý, cần so sánh và quyết định merge. Installer không tự ghi đè các tùy chỉnh đó. Cập nhật skill không tự migrate tài liệu BA cũ.

## 9. Lỗi thường gặp

| Lỗi | Cách xử lý |
| --- | --- |
| Không tìm thấy skill | Kiểm tra đúng project và đúng thư mục của công cụ ở mục 1; mở phiên mới |
| Claude không có `/ba-workflow` | Kiểm tra `.claude/skills/ba-workflow/SKILL.md`; dùng Claude Code local theo hướng dẫn |
| Antigravity không thấy skill | Kiểm tra `.agents/skills` và Customizations; đối chiếu tài liệu phiên bản đang dùng |
| `No module named yaml` / `jsonschema` | Agent đang dùng sai Python; chỉ rõ `.venv/Scripts/python.exe` của Kit |
| `INVALID_CONFIG` sau đổi runtime | Giữ `skill_runtime: codex` theo schema phiên bản hiện tại |
| Thiếu tài nguyên contracts/scripts | Cài bằng installer thay vì chỉ copy SKILL.md |
| `MISSING_INPUT` / `STALE_INPUT` | Chạy bước tạo nguồn còn thiếu hoặc cập nhật/review lại tài liệu phụ thuộc |
| `MISSING_APPROVAL` | Đọc tài liệu/dry-run và quyết định cho checkpoint đang thiếu |
| `PUBLISH_CONFLICT` | So bản cũ/mới và quyết định cách giữ lịch sử trước khi xuất tiếp |

## 10. Kiểm chứng và công cụ nâng cao

**Đã kiểm chứng:** pipeline fixtures, installer vào thư mục tùy chọn, nguồn/schema/publish và discovery đủ 11 skill trên Codex CLI 0.161.0. Thư mục `tests/` và các báo cáo kiểm thử chỉ giữ local để bảo trì, được Git bỏ qua và không đóng gói vào ZIP; không cần chúng khi cài sang máy hoặc project khác.

**Chưa chạy trực tiếp:** discovery và pipeline trong Claude Code/Antigravity. Hai hướng dẫn đó dựa trên định dạng SKILL.md và đường dẫn chính thức; không coi việc file đã cài là bằng chứng agent đã thực hiện thành công. Agent cần có quyền đọc/ghi project và chạy Python theo thiết lập của công cụ.

Các lệnh sau dùng Python của Kit, chạy tại thư mục Kit:

```powershell
.\.venv\Scripts\python.exe scripts/validate_ba_document.py --project-config "D:/Projects/MyProject/.temp/ba-project.yaml" --file ".temp/drafts/PBI-001/spec.md" --expected-type spec --pbi-id PBI-001 --check-refs --format json
.\.venv\Scripts\python.exe scripts/workflow_state.py --project-config "D:/Projects/MyProject/.temp/ba-project.yaml"
.\.venv\Scripts\python.exe scripts/publish_ba.py --project-config "D:/Projects/MyProject/.temp/ba-project.yaml" --pbi-id PBI-001
```

Lệnh publish trên chỉ dry-run; `--apply` chỉ thực hiện khi đã có phê duyệt thật theo hợp đồng Kit. Nếu máy bảo trì còn `tests/`, có thể chạy `python -m unittest discover -s tests -v` để kiểm thử local. Các fixture chứa phê duyệt mô phỏng, không dùng làm phê duyệt dự án thật.

Hướng dẫn nghiệp vụ: [project hiện có](GUIDE_EXISTING_PROJECT.md) hoặc [project mới](GUIDE_NEW_PROJECT.md). Giới thiệu chung: [README](README.md). Chi tiết hợp đồng và bảo toàn dữ liệu: [BA-CONVENTIONS](conventions/BA-CONVENTIONS.md).
