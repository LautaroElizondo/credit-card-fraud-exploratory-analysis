import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Carga ---
df = pd.read_csv("creditcard.csv")  # ajustá la ruta si hace falta
df.groupby("Class")["Amount"].agg(["count", "mean", "median", "max"]).round(2)
# --- Vista general ---
print(df.shape)
print(df.head())
print(df.info())
print(df.describe().T)
print("Nulos:", df.isnull().sum().sum(), "| Duplicados:", df.duplicated().sum())
print(df["Class"].value_counts())

# --- Visualización general ---
fig, ax = plt.subplots(2, 2, figsize=(14, 10))

# 1) Balance de clases
conteo = df["Class"].value_counts()
ax[0, 0].bar(["Normal (0)", "Fraude (1)"], conteo.values, color=["#4C72B0", "#C44E52"])
ax[0, 0].set_yscale("log")
ax[0, 0].set_title("Balance de clases (escala log)")
for i, v in enumerate(conteo.values):
    ax[0, 0].text(i, v, f"{v:,}", ha="center", va="bottom")

# 2) Monto por clase (log1p)
for c, color, lab in [(0, "#4C72B0", "Normal"), (1, "#C44E52", "Fraude")]:
    ax[0, 1].hist(np.log1p(df.loc[df.Class == c, "Amount"]), bins=50,
                  alpha=0.6, density=True, color=color, label=lab)
ax[0, 1].set_title("Distribución del monto, log(1+Amount)")
ax[0, 1].legend()

# 3) Transacciones por hora del día
df["Hora"] = (df["Time"] // 3600) % 24
for c, color, lab in [(0, "#4C72B0", "Normal"), (1, "#C44E52", "Fraude")]:
    ax[1, 0].hist(df.loc[df.Class == c, "Hora"], bins=24, alpha=0.6,
                  density=True, color=color, label=lab)
ax[1, 0].set_title("Transacciones por hora del día (normalizado)")
ax[1, 0].legend()

# 4) Correlación de cada variable con Class
corr = df.drop(columns="Hora").corr()["Class"].drop("Class").sort_values()
ax[1, 1].barh(corr.index, corr.values,
              color=["#C44E52" if x < 0 else "#4C72B0" for x in corr.values])
ax[1, 1].set_title("Correlación con Class")
ax[1, 1].tick_params(axis="y", labelsize=7)

plt.tight_layout()
plt.savefig("vista_general_creditcard.png", dpi=130)
plt.show()

