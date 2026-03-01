import sys
import json
import argparse
import matplotlib.pyplot as plt

def generate_pie(data_json_path, output_path, title_text):
    with open(data_json_path, 'r') as f:
        data = json.load(f)
    
    # Sort data by amount descending
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    labels = [k for k, v in sorted_items]
    sizes = [v for k, v in sorted_items]
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
    fig.set_facecolor('black')
    
    # Optional colors, matplotlib cycle will take over if not enough colors
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f']
    # pad colors if needed
    if len(sizes) > len(colors):
        colors = colors * (len(sizes) // len(colors) + 1)
        
    wedges, texts, autotexts = ax.pie(
        sizes, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors[:len(sizes)],
        textprops={'fontsize': 18, 'color': 'white'},
        radius=0.8
    )
    
    plt.setp(autotexts, size=16, weight="bold")
    
    # Put labels in a legend perfectly aligned below the pie
    ax.legend(wedges, labels,
          loc="lower center",
          bbox_to_anchor=(0.5, -0.2),
          ncol=1,
          fontsize=22,
          frameon=False)
    
    # Replace literal literal \n with actual newlines in string argument if escaped
    title_text = title_text.replace('\\n', '\n')
    
    plt.text(0, 1.3, title_text, 
             ha='center', va='center', fontsize=32, fontweight='bold', color='white')
    
    ax.axis('equal')  
    plt.tight_layout()
    plt.subplots_adjust(top=0.7)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches='tight')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="JSON file with category amounts (dict: string -> float)")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--title", required=True, help="Title text with newlines (use \\n for breaks)")
    args = parser.parse_args()
    generate_pie(args.data, args.output, args.title)
