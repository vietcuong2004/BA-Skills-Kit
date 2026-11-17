# Cập nhật một PBI mới mà giữ hồ sơ hiện tại

## Baseline và ID

Đọc cấu hình, CAP/REQ/EPIC/FEAT/PBI và history trước khi sửa. Lưu baseline SHA-256 theo file và snapshot đối tượng liên quan trong record; giữ baseline ngoài canonical nguồn để tránh source cycle. Không chép dữ liệu riêng tư/secret. So draft chưa publish, lịch sử published và request đang mở để tránh ID collision.

Cấp ID theo prefix cấu hình, giữ tối thiểu ba chữ số, dùng số chưa từng được cấp; không tái sử dụng lỗ hổng số nếu không biết lịch sử. Không “đặt trước” ID trong backlog thật rồi sửa nội dung không liên quan để giữ chỗ. Re-read/hash trước khi ghi nếu có khả năng agent/người khác đang cập nhật; conflict thì dừng và merge có chủ đích.

Nếu REQ đã có trong unassigned_requirements và được PBI mới cover, bỏ đúng entry unassigned sau khi mapping hoàn tất; một REQ không đồng thời covered/unassigned. REQ phục vụ nhiều PBI là hợp lệ nếu scope/giá trị phân biệt được; không nhầm quan hệ nhiều-nhiều với duplicate behavior.

## Khi cần sửa upstream

- Cùng CAP/REQ, chỉ lát cắt chưa có trong backlog: giữ brainstorm/requirements nguyên bytes, dùng lại nguồn.
- Nhu cầu mới trong CAP đã có: cập nhật requirements bằng ba-requirements, bổ sung REQ/rule/flow cần thiết; không đổi nghĩa BR cũ dưới cùng ID khi quyết định khác.
- Ngoài CAP hiện tại: cập nhật brainstorm bằng ba-brainstorm trước, sau đó đọc lại và cập nhật requirements có kiểm soát.
- Giữ schema đầy đủ của toàn tài liệu, không thay cả tài liệu bằng một PBI/REQ mới. PBI mới phải có parent Epic/Feature tồn tại và feature requirement_refs bao phủ requirement_refs PBI.

Mỗi bước đọc nguồn thật đã validate; metadata.generated_by theo bước thực hiện, không đổi enums schema để thêm ba-pbi. ba-pbi điều phối việc thực thi, lưu vào request record để không mạo danh invocation runtime.

## Freshness không chỉ là sửa hash

Backlog đổi bytes → các Round/business/spec/review có hash backlog cũ stale. Requirements/brainstorm đổi → chain ảnh hưởng rộng hơn. Đây là tác động dự kiến của contract hiện tại, phải nói rõ dù các PBI cũ vẫn giữ nguyên nghĩa.

Trong scope thêm một PBI, chỉ rebase những nguồn cần cho PBI đó: đọc lại source mới, đối chiếu nội dung, sửa nếu có ảnh hưởng và validate. Round plan muốn dùng cần giữ allocation cũ, thêm PBI mới vào unassigned hoặc Round được cho phép, cập nhật history/status đúng quyết định; không tự lấy approval của bytes cũ gán cho plan mới.

Các PBI khác: liệt kê stale để người dùng chọn xử lý; không tái tạo tài liệu toàn dự án hoặc refresh hash ngầm. Các file đã publish giữ nguyên, thay đổi có thể khiến validator báo stale và cần một công việc cập nhật riêng. Đừng gọi chúng “hỏng/mất dữ liệu” vì hash nguồn thay đổi.

Nếu scope mới đã được duyệt ngay trong yêu cầu và đủ cụ thể, tái sử dụng quyết định đó; không hỏi lại chỉ vì đi qua tên skill khác. Nhưng user yêu cầu “tạo PBI” chưa duyệt sẵn mọi assumptions AI nêu ra. Báo delta cụ thể để người dùng quyết định.

## Handoff business/spec

Sau khi duyệt backlog delta, đọc SKILL.md của ba-business/ba-spec/ba-review ở các thư mục sibling. Với bản cài, không dùng đường dẫn tương đối về Kit source gốc. Business/spec phải cùng PBI ID/title/parents/requirements/scope với backlog; local AC/EC/Flow IDs thuộc PBI mới.

Không cần ép Round để viết draft nếu user chưa chọn đợt. Omit round_id trong metadata và data khi chưa có allocation; không tạo R0/R1 giả. Review tạo đúng source hashes. Publish là bước riêng, cần Round và approvals hiện hành.
