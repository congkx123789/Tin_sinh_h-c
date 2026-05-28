import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set premium dark style
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.facecolor'] = '#121214'
plt.rcParams['figure.facecolor'] = '#121214'

def draw_system_pipeline():
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#121214')
    ax.set_facecolor('#121214')
    
    stages = [
        {"title": "1. Dữ liệu Đầu vào", "items": ["RNA-Seq thô (TCGA)", "Đột biến DNA (GATK)", "Lâm sàng & Sống sót"], "color": "#EC4899"},
        {"title": "2. Tiền xử lý Sạch", "items": ["Ánh xạ Gene Symbol", "KNN Imputer (K=5)", "Lọc Outliers (I-Forest)"], "color": "#3B82F6"},
        {"title": "3. Chọn Đặc trưng", "items": ["Variance Pre-filter", "Spearman Correlation", "CoxPH L2 Regularization"], "color": "#10B981"},
        {"title": "4. Học máy & Học sâu", "items": ["Ensemble LightGBM (10-Seed)", "DAE-SurvivalMambaNet", "Tối ưu Cox Loss / RMSE"], "color": "#8B5CF6"},
        {"title": "5. Đầu ra Trực quan", "items": ["Streamlit Web Dashboard", "Biểu đồ phân tầng KM", "Báo cáo Cá nhân hóa"], "color": "#F59E0B"}
    ]
    
    box_width = 2.0
    box_height = 2.2
    start_x = -5.0
    spacing = 2.5
    
    for i, stage in enumerate(stages):
        x = start_x + i * spacing
        
        # Rounded box
        rect = patches.FancyBboxPatch(
            (x - box_width/2, -box_height/2), box_width, box_height,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            linewidth=2, edgecolor=stage["color"], facecolor='#1F2937',
            zorder=2
        )
        ax.add_patch(rect)
        
        # Header text
        ax.text(
            x, box_height/2 - 0.2, stage["title"],
            color=stage["color"], fontsize=11, fontweight='bold',
            ha='center', va='center', zorder=3
        )
        
        # Items text
        items_y = [0.4, -0.2, -0.8]
        for j, item in enumerate(stage["items"]):
            ax.text(
                x, items_y[j], f"• {item}",
                color='#E5E7EB', fontsize=9.5,
                ha='center', va='center', zorder=3
            )
            
        # Draw connecting arrow
        if i < len(stages) - 1:
            ax.annotate(
                '',
                xy=(x + box_width/2 + 0.4, 0),
                xytext=(x + box_width/2 + 0.1, 0),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color='#4B5563',
                    lw=2,
                    mutation_scale=15
                ),
                zorder=1
            )
            
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-1.8, 1.8)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('results/system_pipeline.png', dpi=300, facecolor='#121214')
    plt.close()
    print("Generated system_pipeline.png")

def draw_survivalmambanet_architecture():
    fig, ax = plt.subplots(figsize=(13, 7), facecolor='#121214')
    ax.set_facecolor('#121214')
    
    # 1. Draw input
    ax.text(-5.5, 0, "Biểu hiện gen thô\n(16.000+ chiều)", color='#FFFFFF', fontsize=11, fontweight='bold',
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc='#374151', ec='#4B5563', lw=1.5), zorder=2)
    
    # Arrow to DAE
    ax.annotate('', xy=(-3.8, 0), xytext=(-4.5, 0), arrowprops=dict(arrowstyle="-|>", color='#6B7280', lw=2, mutation_scale=15))
    
    # 2. DAE Box
    dae_box = patches.FancyBboxPatch((-3.6, -1.8), 2.2, 3.6, boxstyle="round,pad=0.1", lw=2, edgecolor='#3B82F6', facecolor='#1E293B', zorder=1)
    ax.add_patch(dae_box)
    ax.text(-2.5, 1.5, "1. Denoising Autoencoder (DAE)", color='#3B82F6', fontsize=11, fontweight='bold', ha='center', va='center', zorder=2)
    
    dae_layers = [
        {"name": "Input + Noise (0.2)", "y": 0.9, "color": "#475569"},
        {"name": "Encoder Layer 1 (512)", "y": 0.3, "color": "#1E3A8A"},
        {"name": "Encoder Layer 2 (256)", "y": -0.3, "color": "#1E3A8A"},
        {"name": "Latent Space (128)", "y": -0.9, "color": "#0369A1"}
    ]
    for layer in dae_layers:
        ax.text(-2.5, layer["y"], layer["name"], color='#FFFFFF', fontsize=9.5, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", fc=layer["color"], ec='none'), zorder=2)
        
    # Arrow from DAE to Mamba
    ax.annotate('', xy=(-0.8, 0), xytext=(-1.2, 0), arrowprops=dict(arrowstyle="-|>", color='#6B7280', lw=2, mutation_scale=15))
    
    # 3. Mamba Box
    mamba_box = patches.FancyBboxPatch((-0.6, -1.8), 2.2, 3.6, boxstyle="round,pad=0.1", lw=2, edgecolor='#10B981', facecolor='#064E3B', zorder=1)
    ax.add_patch(mamba_box)
    ax.text(0.5, 1.5, "2. Survival Mamba Block (SSM)", color='#10B981', fontsize=11, fontweight='bold', ha='center', va='center', zorder=2)
    
    mamba_steps = [
        {"name": "State Expansion", "y": 0.6},
        {"name": "Selective Scan SSM", "y": 0.0},
        {"name": "Linear Projection", "y": -0.6}
    ]
    for step in mamba_steps:
        ax.text(0.5, step["y"], step["name"], color='#FFFFFF', fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.4", fc='#022C22', ec='#10B981', lw=1), zorder=2)
        
    # Arrow from Mamba to Output
    ax.annotate('', xy=(2.2, 0), xytext=(1.8, 0), arrowprops=dict(arrowstyle="-|>", color='#6B7280', lw=2, mutation_scale=15))
    
    # 4. Output Risk Score
    ax.text(3.2, 0, "Chỉ số Rủi ro\n(Risk Score - h)", color='#FFFFFF', fontsize=11, fontweight='bold',
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc='#7F1D1D', ec='#EF4444', lw=1.5), zorder=2)
            
    # Arrow to Loss
    ax.annotate('', xy=(4.6, 0), xytext=(4.2, 0), arrowprops=dict(arrowstyle="-|>", color='#6B7280', lw=2, mutation_scale=15))
    
    # 5. Loss Box
    loss_box = patches.FancyBboxPatch((4.8, -1.2), 1.8, 2.4, boxstyle="round,pad=0.1", lw=2, edgecolor='#EF4444', facecolor='#1F1616', zorder=1)
    ax.add_patch(loss_box)
    ax.text(5.7, 0.9, "Cox Loss Function", color='#EF4444', fontsize=11, fontweight='bold', ha='center', va='center', zorder=2)
    ax.text(5.7, 0.2, "Xử lý khuyết góc\n(Censored)", color='#E5E7EB', fontsize=9.5, ha='center', va='center', zorder=2)
    ax.text(5.7, -0.5, "Tối ưu hóa trực tiếp\nthứ tự sinh tồn", color='#E5E7EB', fontsize=9.5, ha='center', va='center', zorder=2)
    
    ax.set_xlim(-6.8, 7.0)
    ax.set_ylim(-2.2, 2.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('results/survivalmambanet_architecture.png', dpi=300, facecolor='#121214')
    plt.close()
    print("Generated survivalmambanet_architecture.png")

if __name__ == "__main__":
    draw_system_pipeline()
    draw_survivalmambanet_architecture()
