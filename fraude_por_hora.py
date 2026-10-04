import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# df ya debe estar cargado: df = pd.read_csv("creditcard.csv")

# --- Nuevas columnas ---
df["hora"] = df["Time"] / 3600                   # horas transcurridas (0 a ~48)
df["hora_entera"] = df["hora"].astype(int)       # 0 a 47 (hora transcurrida, redondeada hacia abajo)
df["hora_dia"] = df["hora_entera"] % 24          # 0 a 23 (hora del día, asumiendo que Time=0 es medianoche)

# --- Tablas de resumen ---
por_hora = (df.groupby(["hora_entera", "Class"]).size()
              .unstack(fill_value=0)
              .rename(columns={0: "normales", 1: "fraudes"}))
por_hora["total"] = por_hora["normales"] + por_hora["fraudes"]
por_hora["pct_fraude"] = (por_hora["fraudes"] / por_hora["total"] * 100).round(3)

por_hora_dia = (df.groupby(["hora_dia", "Class"]).size()
                  .unstack(fill_value=0)
                  .rename(columns={0: "normales", 1: "fraudes"}))
por_hora_dia["total"] = por_hora_dia["normales"] + por_hora_dia["fraudes"]
por_hora_dia["pct_fraude"] = (por_hora_dia["fraudes"] / por_hora_dia["total"] * 100).round(3)

print("Top 10 horas (0-47) con más fraudes:")
print(por_hora.sort_values("fraudes", ascending=False).head(10))
print("\nTop 5 horas del día (0-23) con más fraudes:")
print(por_hora_dia.sort_values("fraudes", ascending=False).head(5))

# --- Gráficos ---
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(13, 13))

# 1) Cantidad de transacciones por hora de reloj, normales vs fraudes (proporción dentro de cada clase)
prop = df.groupby("Class")["hora_dia"].value_counts(normalize=True).rename("prop").reset_index()
prop["Tipo"] = prop["Class"].map({0: "Normal", 1: "Fraude"})
sns.barplot(data=prop, x="hora_dia", y="prop", hue="Tipo",
            palette={"Normal": "#4C72B0", "Fraude": "#C44E52"}, ax=axes[0])
axes[0].set_title("Distribución por hora del día (proporción dentro de cada clase)")
axes[0].set_xlabel("Hora del día (0-23)")
axes[0].set_ylabel("Proporción")

# 2) Cantidad de fraudes por hora transcurrida (0-47)
axes[1].bar(por_hora.index, por_hora["fraudes"], color="#C44E52")
axes[1].set_title("Cantidad de fraudes por hora transcurrida (0-47)")
axes[1].set_xlabel("Horas desde la primera transacción")
axes[1].set_ylabel("Nº de fraudes")
axes[1].set_xticks(range(0, 48, 2))

# 3) Tasa de fraude (% sobre el total de transacciones de esa hora)
axes[2].plot(por_hora.index, por_hora["pct_fraude"], marker="o", color="#8172B2")
axes[2].set_title("Tasa de fraude por hora transcurrida (% de las transacciones de esa hora)")
axes[2].set_xlabel("Horas desde la primera transacción")
axes[2].set_ylabel("% fraude")
axes[2].set_xticks(range(0, 48, 2))

plt.tight_layout()
plt.savefig("fraude_por_hora.png", dpi=130)
plt.show()
