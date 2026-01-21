from sqlmodel import Session, select
from src.models import Role, RoleName, Utilisateur, Objet, Poids, Vignette, Commune, Departement, Conditionnement
from src.core.auth.security import get_password_hash
from decimal import Decimal



class SeedService:
    def __init__(self, db: Session):
        self.db = db

    # -----------------------
    # PUBLIC ENTRYPOINT
    # -----------------------
    def run(self):
        print("🌱 Seeding database...")
        role_map = self._seed_roles()
        self._seed_users(role_map)
        self._seed_departements()
        self._seed_objets()
        self._seed_poids()
        self._seed_vignettes()
        self._seed_conditionnements()
        print("🌱 Seeding terminé avec succès")

    # -----------------------
    # ROLES
    # -----------------------
    def _seed_roles(self):
        roles_to_create = [
            RoleName.ADMIN,
            RoleName.OPERATEUR_COLIS,
            RoleName.OPERATEUR_STOCK
        ]

        existing_roles = self.db.exec(select(Role)).all()
        existing_role_names = {r.librole for r in existing_roles}

        role_map = {}

        for role_name in roles_to_create:
            if role_name not in existing_role_names:
                role = Role(librole=role_name)
                self.db.add(role)
                self.db.commit()
                self.db.refresh(role)
                print(f"✅ Role créé : {role_name}")
                role_map[role_name] = role
            else:
                role = self.db.exec(
                    select(Role).where(Role.librole == role_name)
                ).first()
                role_map[role_name] = role
                print(f"ℹ️ Role existe déjà : {role_name}")

        return role_map

    # -----------------------
    # USERS
    # -----------------------
    def _seed_users(self, role_map):
        users_to_create = [
            {
                "username": "admin",
                "password": "admin123",
                "nom": "Admin",
                "prenom": "System",
                "roles": [RoleName.ADMIN]
            },
            {
                "username": "colis",
                "password": "colis123",
                "nom": "Operateur",
                "prenom": "Colis",
                "roles": [RoleName.OPERATEUR_COLIS]
            },
            {
                "username": "stock",
                "password": "stock123",
                "nom": "Operateur",
                "prenom": "Stock",
                "roles": [RoleName.OPERATEUR_STOCK]
            }
        ]

        for user_data in users_to_create:
            existing_user = self.db.exec(
                select(Utilisateur).where(
                    Utilisateur.username == user_data["username"]
                )
            ).first()

            if existing_user:
                print(f"ℹ️ Utilisateur existe déjà : {user_data['username']}")
                continue

            user = Utilisateur(
                username=user_data["username"],
                password=get_password_hash(user_data["password"]),
                nom_utilisateur=user_data["nom"],
                prenom_utilisateur=user_data["prenom"],
                disabled=False
            )

            for role_name in user_data["roles"]:
                user.roles.append(role_map[role_name])

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            print(f"✅ Utilisateur créé : {user.username}")



 # -----------------------
    # DEPARTEMENTS & COMMUNES
    # -----------------------
    def _seed_departements(self):
        # Exemple de départements et communes
        departements_to_create = [
            {
                "code": "75",
                "nom": "Paris",
                "ordre_aff": 1,
                "communes": [
                    {"cp": "75001", "nom": "Paris 1er Arrondissement"},
                    {"cp": "75002", "nom": "Paris 2e Arrondissement"}
                ]
            },
            {
                "code": "69",
                "nom": "Rhône",
                "ordre_aff": 2,
                "communes": [
                    {"cp": "69001", "nom": "Lyon 1er Arrondissement"},
                    {"cp": "69002", "nom": "Lyon 2e Arrondissement"}
                ]
            }
        ]

        for dep_data in departements_to_create:
            existing_dep = self.db.exec(
                select(Departement).where(Departement.code == dep_data["code"])
            ).first()

            if existing_dep:
                print(f"ℹ️ Département existe déjà : {dep_data['nom']}")
                continue

            dep = Departement(
                code=dep_data["code"],
                nom=dep_data["nom"],
                ordre_aff=dep_data["ordre_aff"]
            )

            # Ajouter les communes
            for commune_data in dep_data["communes"]:
                commune = Commune(
                    cp=commune_data["cp"],
                    nom=commune_data["nom"]
                )
                dep.communes.append(commune)

            self.db.add(dep)
            self.db.commit()
            self.db.refresh(dep)
            print(f"✅ Département créé : {dep.nom} avec {len(dep.communes)} communes")

    

# -----------------------
    # OBJETS
    # -----------------------
    def _seed_objets(self):
        objets_to_create = [
            {
                "libobj": "Fromage Camembert",
                "tailleobj": "250g",
                "puobj": Decimal("5.50"),
                "poidsobj": Decimal("0.25"),
                "indispobj": 0,
                "o_imp": 1,
                "o_aff": 1,
                "points": 10,
                "o_ordre_aff": 1
            },
            {
                "libobj": "Fromage Brie",
                "tailleobj": "300g",
                "puobj": Decimal("6.00"),
                "poidsobj": Decimal("0.3"),
                "indispobj": 0,
                "o_imp": 1,
                "o_aff": 1,
                "points": 12,
                "o_ordre_aff": 2
            }
        ]

        for obj_data in objets_to_create:
            existing_obj = self.db.exec(
                select(Objet).where(Objet.libobj == obj_data["libobj"])
            ).first()

            if existing_obj:
                print(f"ℹ️ Objet existe déjà : {obj_data['libobj']}")
                continue

            obj = Objet(**obj_data)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            print(f"✅ Objet créé : {obj.libobj}")


 # -----------------------
    # POIDS
    # -----------------------
    def _seed_poids(self):
        poids_to_create = [
            {"min": Decimal("0"), "value": Decimal("2.50")},
            {"min": Decimal("5"), "value": Decimal("5.00")},
            {"min": Decimal("10"), "value": Decimal("7.50")},
            {"min": Decimal("20"), "value": Decimal("12.00")},
        ]

        for poids_data in poids_to_create:
            # Vérifier si le poids existe déjà (par la valeur)
            existing = self.db.exec(
                select(Poids).where(Poids.value == poids_data["value"])
            ).first()

            if existing:
                print(f"ℹ️ Poids existe déjà : {poids_data['value']}")
                continue

            poids = Poids(**poids_data)
            self.db.add(poids)
            self.db.commit()
            self.db.refresh(poids)
            print(f"✅ Poids créé : min={poids.min}, value={poids.value}")


# -----------------------
    # VIGNETTES
    # -----------------------
    def _seed_vignettes(self):
        vignettes_to_create = [
            {"min": Decimal("0"), "value": Decimal("1.50")},
            {"min": Decimal("5"), "value": Decimal("2.50")},
            {"min": Decimal("10"), "value": Decimal("3.50")},
            {"min": Decimal("20"), "value": Decimal("5.00")},
        ]

        for vignette_data in vignettes_to_create:
            # Vérifier si la vignette existe déjà (par la valeur)
            existing = self.db.exec(
                select(Vignette).where(Vignette.value == vignette_data["value"])
            ).first()

            if existing:
                print(f"ℹ️ Vignette existe déjà : {vignette_data['value']}")
                continue

            vignette = Vignette(**vignette_data)
            self.db.add(vignette)
            self.db.commit()
            self.db.refresh(vignette)
            print(f"✅ Vignette créée : min={vignette.min}, value={vignette.value}")



 # -----------------------
    # CONDITIONNEMENTS
    # -----------------------
    def _seed_conditionnements(self):
        conditionnements_to_create = [
            {"libelle": "Boîte standard", "poids": 500, "prix": Decimal("2.50"), "ordreimp": 1},
            {"libelle": "Sac kraft", "poids": 1000, "prix": Decimal("3.50"), "ordreimp": 2},
            {"libelle": "Carton 5kg", "poids": 5000, "prix": Decimal("10.00"), "ordreimp": 3},
        ]

        for cond_data in conditionnements_to_create:
            # Vérifier si le conditionnement existe déjà (par libelle)
            existing = self.db.exec(
                select(Conditionnement).where(Conditionnement.libelle == cond_data["libelle"])
            ).first()

            if existing:
                print(f"ℹ️ Conditionnement existe déjà : {cond_data['libelle']}")
                continue

            cond = Conditionnement(**cond_data)
            self.db.add(cond)
            self.db.commit()
            self.db.refresh(cond)
            print(f"✅ Conditionnement créé : {cond.libelle}, poids={cond.poids}, prix={cond.prix}")

