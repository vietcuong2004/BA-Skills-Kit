# Xem trước hoặc xuất PBI

Xuất tài liệu bằng lệnh sau. Helper kiểm nguồn và đích trước khi ghi.

```powershell
python "<KIT_ROOT>/scripts/publish_ba.py" --project-config "<PROJECT>/.temp/ba-project.yaml" --pbi-id PBI-001 --apply
```

Bỏ --apply khi chỉ muốn xem trước. Kết quả xem trước có đường dẫn đích, hành động và hash từng file, cùng kết quả review và lỗi nếu có. Khi hai file đích trùng nội dung thì helper báo skip.
