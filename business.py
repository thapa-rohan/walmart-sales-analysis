import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/Users/rohanthapa/Desktop/project/walmart.csv')

# ── PHASE 2: CLEAN ──────────────────────────
df['unit_price'] = df['unit_price'].str.replace('$', '', regex=False)
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
df['quantity'] = df['quantity'].fillna(df['quantity'].median())
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M').astype(str)
df['total_sales'] = df['unit_price'] * df['quantity']

# ── PHASE 3: ANALYSIS ───────────────────────
cat_sales  = df.groupby('category')['total_sales'].sum().sort_values(ascending=False)
city_sales = df.groupby('City')['total_sales'].sum().sort_values(ascending=False)
cat_rating = df.groupby('category')['rating'].mean().sort_values(ascending=False)
cat_profit = df.groupby('category')['profit_margin'].mean().sort_values(ascending=False)
monthly    = df.groupby('month')['total_sales'].sum().sort_index()

print("=== KEY FINDINGS ===")
print(f"Best selling category:  {cat_sales.index[0]} (${cat_sales.iloc[0]:,.0f})")
print(f"Worst selling category: {cat_sales.index[-1]} (${cat_sales.iloc[-1]:,.0f})")
print(f"Highest rated category: {cat_rating.index[0]} ({cat_rating.iloc[0]:.2f}/10)")
print(f"Lowest rated category:  {cat_rating.index[-1]} ({cat_rating.iloc[-1]:.2f}/10)")
print(f"Best profit margin:     {cat_profit.index[0]} ({cat_profit.iloc[0]:.2f})")
print(f"Worst profit margin:    {cat_profit.index[-1]} ({cat_profit.iloc[-1]:.2f})")
print(f"Top city by sales:      {city_sales.index[0]} (${city_sales.iloc[0]:,.0f})")

# ── PHASE 4: CHARTS ─────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Walmart Sales — Business Case Analysis', fontsize=18, fontweight='bold')

# Chart 1: Sales by category
c1 = ['#2ecc71' if i == 0 else '#e74c3c' if i == len(cat_sales)-1 else '#3498db' for i in range(len(cat_sales))]
axes[0,0].barh(cat_sales.index, cat_sales.values, color=c1)
axes[0,0].set_title('Total Sales by Category', fontweight='bold')
axes[0,0].set_xlabel('Total Sales ($)')
for i, v in enumerate(cat_sales.values):
    axes[0,0].text(v + 1000, i, f'${v:,.0f}', va='center', fontsize=8)

# Chart 2: Top 10 cities
top10 = city_sales.head(10)
axes[0,1].barh(top10.index, top10.values, color='#9b59b6')
axes[0,1].set_title('Top 10 Cities by Sales', fontweight='bold')
axes[0,1].set_xlabel('Total Sales ($)')

# Chart 3: Rating by category
c3 = ['#2ecc71' if i == 0 else '#e74c3c' if i == len(cat_rating)-1 else '#f39c12' for i in range(len(cat_rating))]
axes[0,2].bar(range(len(cat_rating)), cat_rating.values, color=c3)
axes[0,2].set_xticks(range(len(cat_rating)))
axes[0,2].set_xticklabels(cat_rating.index, rotation=45, ha='right', fontsize=8)
axes[0,2].set_title('Avg Customer Rating by Category', fontweight='bold')
axes[0,2].set_ylabel('Rating (out of 10)')
axes[0,2].set_ylim(0, 10)
for i, v in enumerate(cat_rating.values):
    axes[0,2].text(i, v + 0.1, f'{v:.1f}', ha='center', fontsize=9)

# Chart 4: Profit margin
c4 = ['#2ecc71' if i == 0 else '#e74c3c' if i == len(cat_profit)-1 else '#1abc9c' for i in range(len(cat_profit))]
axes[1,0].bar(range(len(cat_profit)), cat_profit.values, color=c4)
axes[1,0].set_xticks(range(len(cat_profit)))
axes[1,0].set_xticklabels(cat_profit.index, rotation=45, ha='right', fontsize=8)
axes[1,0].set_title('Avg Profit Margin by Category', fontweight='bold')
axes[1,0].set_ylabel('Profit Margin')
for i, v in enumerate(cat_profit.values):
    axes[1,0].text(i, v + 0.001, f'{v:.3f}', ha='center', fontsize=9)

# Chart 5: Monthly trend
axes[1,1].plot(range(len(monthly)), monthly.values, marker='o', color='#2980b9', linewidth=2)
axes[1,1].set_xticks(range(len(monthly)))
axes[1,1].set_xticklabels(monthly.index, rotation=45, ha='right', fontsize=7)
axes[1,1].set_title('Monthly Sales Trend', fontweight='bold')
axes[1,1].set_ylabel('Total Sales ($)')
axes[1,1].fill_between(range(len(monthly)), monthly.values, alpha=0.15, color='#2980b9')

# Chart 6: Rating vs Sales bubble
axes[1,2].scatter(cat_rating.values, cat_sales.values, s=cat_profit.values*3000,
                  color=['#e74c3c','#f39c12','#2ecc71','#3498db','#9b59b6','#1abc9c'], alpha=0.7)
for i, cat in enumerate(cat_rating.index):
    axes[1,2].annotate(cat, (cat_rating[cat], cat_sales[cat]),
                       textcoords="offset points", xytext=(5,5), fontsize=7)
axes[1,2].set_xlabel('Avg Customer Rating')
axes[1,2].set_ylabel('Total Sales ($)')
axes[1,2].set_title('Rating vs Sales by Category', fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rohanthapa/Desktop/project/walmart_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nChart saved to your project folder!")