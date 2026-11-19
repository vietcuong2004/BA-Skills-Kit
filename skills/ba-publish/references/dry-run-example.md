# Dry-run và checkpoint

```powershell
python "<KIT_ROOT>/scripts/publish_ba.py" --project-config "<PROJECT>/.temp/ba-project.yaml" --pbi-id PBI-001
```

Kết quả có pbi_id, round_id, target, format=pbi-template-v1, entries (`source`, `source_sha256`, `destination`, `sha256`, `action`), blocked, snapshot, config_sha256. source_sha256 là hash draft có metadata trong .temp; sha256 là hash bản đọc được sẽ xuất. Chưa có approval → vẫn trả manifest khi các tài liệu hợp lệ, blocked=MISSING_APPROVAL và exit code 1; không ghi gì.

Ví dụ target `.specify/R1/PBI-001-tao-ghi-chu/`, entries create business.md/spec.md không có front matter/BA-DATA/Contract Summary. Nếu bản đã có đúng bytes của bản render, cả hai action=skip. Nếu một file khác bytes hoặc có file thứ ba, PUBLISH_CONFLICT; helper không hỗ trợ overwrite.

Sau quyết định thật và approval record, chạy lại lệnh có `--apply`. Không tạo approval bằng “TEST HUMAN DOUBLE”; tên đó dành riêng tests. Cờ --apply tự nó không thay được record checkpoint.
