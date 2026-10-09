"""
Script para resetar as tabelas de dados do Roadmap Project,
preservando a tabela de 'users' e o controle de migrações ('alembic_version').
"""
import sys
from sqlalchemy import text
from app.db.session import engine

# Tabelas que serão limpas (zeradas)
TABLES_TO_TRUNCATE = [
    "active_timers",
    "time_entries",
    "audit_logs",
    "activities",
    "deliverables",
    "projects",
    "areas",  # comente ou passe --keep-areas se desejar preservar as áreas
]

def reset_database(keep_areas: bool = False):
    tables = [t for t in TABLES_TO_TRUNCATE if not (keep_areas and t == "areas")]
    
    print("\n" + "=" * 60)
    print("🧹 RESET DO BANCO DE DADOS (ROADMAP)")
    print("=" * 60)
    print(f"Tabelas que serão limpas: {', '.join(tables)}")
    print("Tabelas que serão MANTIDAS: users, alembic_version" + (", areas" if keep_areas else ""))
    print("=" * 60)

    with engine.begin() as conn:
        # Desabilita temporariamente checagem de foreign keys
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        for table in tables:
            try:
                conn.execute(text(f"DELETE FROM `{table}`;"))
                conn.execute(text(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1;"))
                print(f"✔ Tabela '{table}' limpa com sucesso (IDs resetados para 1).")
            except Exception as e:
                print(f"✖ Erro ao limpar '{table}': {e}")
        
        # Reativa checagem de foreign keys
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    print("\n✅ Reset concluído com sucesso!")
    print("A tabela 'users' foi mantida intacta com todos os logins e permissões.\n")

if __name__ == "__main__":
    keep_areas_flag = "--keep-areas" in sys.argv
    reset_database(keep_areas=keep_areas_flag)

