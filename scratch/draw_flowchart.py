import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up figure and axis with a premium dark theme
fig, ax = plt.subplots(figsize=(10, 12), facecolor='#121214')
ax.set_facecolor('#121214')

# Define steps
steps = [
    {"title": "Dữ liệu RNA-Seq thô", "desc": "16.000+ gen, dữ liệu biểu hiện thô từ TCGA", "color": "#4B5563", "text_color": "#F3F4F6"},
    {"title": "1. Lọc biểu hiện & biến thiên thấp", "desc": "Giảm nhiễu, loại bỏ các gen ít thay đổi", "color": "#3B82F6", "text_color": "#FFFFFF"},
    {"title": "2. Nội suy dữ liệu khuyết", "desc": "KNN Imputer (K=5) dựa trên khoảng cách Euclid", "color": "#10B981", "text_color": "#FFFFFF"},
    {"title": "3. Loại bỏ mẫu dị biệt", "desc": "Isolation Forest (contamination=5%) lọc mẫu lỗi", "color": "#F59E0B", "text_color": "#FFFFFF"},
    {"title": "4. Biến đổi Log1p", "desc": "np.log1p(x) làm mượt phân phối lệch phải", "color": "#8B5CF6", "text_color": "#FFFFFF"},
    {"title": "5. Chuẩn hóa Robust Scaler", "desc": "Căn chỉnh thang đo bằng Median & IQR chống outliers", "color": "#EC4899", "text_color": "#FFFFFF"},
    {"title": "Dữ liệu biểu hiện gen đã xử lý", "desc": "Sẵn sàng đưa vào huấn luyện mô hình", "color": "#059669", "text_color": "#FFFFFF"}
]

n_steps = len(steps)
box_width = 7.5
box_height = 1.0
start_y = 11.0
spacing = 1.6

# Draw boxes and arrows
for i, step in enumerate(steps):
    y = start_y - i * spacing
    
    # Draw rounded box
    rect = patches.FancyBboxPatch(
        (-box_width/2, y - box_height/2), box_width, box_height,
        boxstyle="round,pad=0.1,rounding_size=0.15",
        linewidth=1.5, edgecolor=step["color"], facecolor='#1F2937',
        mutation_scale=1.0, zorder=2
    )
    ax.add_patch(rect)
    
    # Left colored accent line
    accent = patches.Rectangle(
        (-box_width/2, y - box_height/2 + 0.05), 0.15, box_height - 0.1,
        color=step["color"], zorder=3
    )
    ax.add_patch(accent)
    
    # Text inside box
    ax.text(
        -box_width/2 + 0.4, y + 0.15, step["title"],
        color=step["text_color"], fontsize=14, fontweight='bold',
        ha='left', va='center', zorder=4, fontname='DejaVu Sans'
    )
    ax.text(
        -box_width/2 + 0.4, y - 0.2, step["desc"],
        color='#9CA3AF', fontsize=10.5,
        ha='left', va='center', zorder=4, fontname='DejaVu Sans'
    )
    
    # Draw arrow to next step
    if i < n_steps - 1:
        arrow_y = y - box_height/2
        arrow_len = spacing - box_height
        ax.annotate(
            '',
            xy=(0, arrow_y - arrow_len),
            xytext=(0, arrow_y),
            arrowprops=dict(
                arrowstyle="-|>",
                color=step["color"],
                lw=2.5,
                mutation_scale=20,
                patchA=None, patchB=None
            ),
            zorder=1
        )

# Set axis limits and hide them
ax.set_xlim(-5, 5)
ax.set_ylim(start_y - (n_steps - 1) * spacing - 1.0, start_y + 1.0)
ax.axis('off')

# Save to file
output_path = 'results/preprocessing_logic.png'
plt.tight_layout()
plt.savefig(output_path, dpi=300, facecolor='#121214', edgecolor='none')
print(f"Flowchart successfully saved to {output_path}")
