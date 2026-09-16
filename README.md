# pmnm-hocphan

Trần Hiếu Trung Nguyên - 23T1020350 - K47B

1.1
Tôi muốn học về phần mềm mã nguồn mở vì đây là nền tảng của rất nhiều công nghệ hiện đại mà tôi sử dụng hằng ngày, từ hệ điều hành, trình duyệt cho đến các công cụ lập trình. Hiểu về mã nguồn mở giúp tôi nắm được cách cộng đồng lập trình viên trên toàn thế giới hợp tác xây dựng phần mềm minh bạch, an toàn và miễn phí. Ngoài ra, việc học mã nguồn mở còn mở ra cơ hội để tôi đọc, chỉnh sửa và đóng góp vào các dự án thực tế, từ đó nâng cao kỹ năng lập trình, tư duy giải quyết vấn đề và làm việc nhóm. Đây cũng là cách tiết kiệm chi phí đáng kể so với phần mềm thương mại, đồng thời giúp tôi hiểu sâu hơn về các mô hình giấy phép và quyền sử dụng phần mềm trong thực tế.

5 phần mềm mã nguồn mở đang sử dụng hằng ngày:

Linux (Ubuntu) – Giấy phép: GNU GPL v2
Mozilla Firefox – Giấy phép: Mozilla Public License (MPL) 2.0
LibreOffice – Giấy phép: Mozilla Public License (MPL) v2.0
VS Code (mã nguồn – Code OSS) – Giấy phép: MIT License
GIMP – Giấy phép: GNU GPL v3

1.2
Báo cáo phân tích: Sự phân nhánh (fork) của OpenOffice.org thành LibreOffice

Bối cảnh dự án

OpenOffice.org là bộ phần mềm văn phòng mã nguồn mở nổi tiếng, ra đời từ mã nguồn StarOffice được Sun Microsystems công bố năm 2000. Trong suốt một thập kỷ, dự án phát triển mạnh mẽ nhờ sự đóng góp của cộng đồng lập trình viên toàn cầu, trở thành đối thủ cạnh tranh đáng kể với Microsoft Office. Tuy nhiên, năm 2010, khi Oracle mua lại Sun Microsystems, dự án bắt đầu rơi vào khủng hoảng quản trị nghiêm trọng.

Nguyên nhân dẫn đến mâu thuẫn

Mâu thuẫn xuất phát từ cách Oracle quản lý dự án sau khi tiếp quản. Cộng đồng phát triển OpenOffice.org từ lâu đã bất mãn với việc Sun (và sau đó là Oracle) giữ quyền kiểm soát gần như tuyệt đối đối với mã nguồn, thương hiệu và quy trình đóng góp. Các lập trình viên bên ngoài muốn đóng góp mã nguồn phải ký thỏa thuận chuyển nhượng bản quyền cho công ty chủ quản, điều này khiến nhiều nhà phát triển cảm thấy công sức của họ không thực sự thuộc về cộng đồng mở mà bị doanh nghiệp hóa.

Khi Oracle tiếp quản, tình hình trở nên tồi tệ hơn. Oracle nổi tiếng với chiến lược ưu tiên lợi nhuận từ phần mềm thương mại, và ít đầu tư vào phát triển cộng đồng mã nguồn mở. Nhiều nhà phát triển lo ngại Oracle sẽ giảm đầu tư, làm chậm tốc độ phát hành, hoặc thậm chí thương mại hóa hoàn toàn dự án. Sự thiếu minh bạch trong định hướng chiến lược của Oracle càng làm gia tăng sự ngờ vực từ cộng đồng.

Sự ra đời của LibreOffice

Trước tình hình đó, vào tháng 9 năm 2010, một nhóm các nhà phát triển kỳ cựu của OpenOffice.org đã quyết định tách nhánh (fork) mã nguồn để thành lập một dự án độc lập mang tên LibreOffice, dưới sự bảo trợ của một tổ chức phi lợi nhuận mới thành lập: The Document Foundation. Mục tiêu của họ là đảm bảo dự án được quản trị theo mô hình cộng đồng thực sự, không phụ thuộc vào bất kỳ công ty đơn lẻ nào, đồng thời loại bỏ yêu cầu chuyển nhượng bản quyền gây tranh cãi.

Ban đầu, The Document Foundation từng mời Oracle tham gia với tư cách thành viên sáng lập, nhưng Oracle từ chối và tiếp tục duy trì OpenOffice.org theo cách riêng. Tuy nhiên, chỉ vài tháng sau, vào tháng 4 năm 2011, Oracle tuyên bố ngừng phát triển thương mại OpenOffice.org và trao mã nguồn cho Apache Software Foundation, dẫn đến sự ra đời của Apache OpenOffice.

Hậu quả và bài học

Kết quả của cuộc phân nhánh này là sự phân tán nguồn lực cộng đồng. Phần lớn các nhà phát triển tích cực, doanh nghiệp tài trợ và các bản phân phối Linux lớn (như Ubuntu, Debian, Fedora) đã chuyển sang hỗ trợ LibreOffice, khiến dự án này nhanh chóng vượt qua OpenOffice.org về tốc độ phát triển, số lượng tính năng mới và mức độ phổ biến. Ngược lại, Apache OpenOffice dần trở nên trì trệ, với chu kỳ phát hành chậm chạp và ít thay đổi đáng kể trong nhiều năm, dù về mặt kỹ thuật dự án vẫn tồn tại.

Trường hợp này minh họa rõ ràng rằng cấu trúc quản trị và niềm tin cộng đồng là yếu tố sống còn đối với một dự án mã nguồn mở, đôi khi quan trọng hơn cả chất lượng kỹ thuật. Khi quyền lực quản trị tập trung vào một thực thể thương mại thiếu minh bạch, nguy cơ phân nhánh là rất cao, vì cộng đồng luôn có quyền "vote bằng chân" — tức là chuyển sang một nhánh khác nếu họ cảm thấy dự án gốc không còn phục vụ lợi ích chung. Bài học rút ra là các dự án mã nguồn mở cần có cơ chế quản trị minh bạch, phi tập trung và có sự tham gia thực chất của cộng đồng để duy trì tính bền vững lâu dài.
