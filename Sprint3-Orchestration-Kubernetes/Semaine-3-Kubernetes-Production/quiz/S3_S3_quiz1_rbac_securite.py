"""
Quiz 1 - RBAC et Sécurité Kubernetes
Concepts de sécurité et contrôle d'accès

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 25 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 3 - Kubernetes Production
"""

def run_quiz():
    """Execute le quiz de validation des concepts RBAC et sécurité Kubernetes"""

    print("=" * 60)
    print(" QUIZ KUBERNETES PRODUCTION - RBAC ET SÉCURITÉ")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - RBAC de base
    print("\n1. Que signifie RBAC dans Kubernetes ?")
    print("a) Role-Based Access Control  b) Resource-Based Access Control")
    print("c) Rule-Based Access Control  d) Route-Based Access Control")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) RBAC = Role-Based Access Control")

    # Question 2 - ServiceAccount
    print("\n2. Quelle ressource Kubernetes représente une identité pour les processus dans les pods ?")
    print("a) User  b) ServiceAccount  c) Role  d) Secret")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ServiceAccount est l'identité des processus dans les pods")

    # Question 3 - Role vs ClusterRole
    print("\n3. Quelle différence entre Role et ClusterRole ?")
    print("a) Aucune  b) Role=namespace, ClusterRole=cluster")
    print("c) Role=lecture, ClusterRole=écriture  d) Role=dev, ClusterRole=prod")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Role est limité à un namespace, ClusterRole au cluster entier")

    # Question 4 - Bindings
    print("\n4. Comment lier un Role à un ServiceAccount ?")
    print("a) RoleBinding  b) ClusterRoleBinding  c) PolicyBinding  d) ServiceBinding")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) RoleBinding lie un Role à des sujets dans un namespace")

    # Question 5 - Verbes RBAC
    print("\n5. Quels sont les verbes RBAC standard dans Kubernetes ?")
    print("a) read, write, execute  b) get, list, create, update, delete")
    print("c) select, insert, update  d) allow, deny, audit")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) get, list, watch, create, update, patch, delete sont les verbes standard")

    # Question 6 - Principe du moindre privilège
    print("\n6. Le principe du moindre privilège en RBAC signifie :")
    print("a) Donner tous les droits  b) Donner le minimum nécessaire")
    print("c) Donner des droits temporaires  d) Donner des droits aléatoires")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Accorder uniquement les permissions strictement nécessaires")

    # Question 7 - Pod Security Standards
    print("\n7. Quels sont les trois niveaux de Pod Security Standards ?")
    print("a) Low, Medium, High  b) Basic, Standard, Advanced")
    print("c) Privileged, Baseline, Restricted  d) Open, Secure, Locked")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Privileged, Baseline, Restricted sont les trois niveaux")

    # Question 8 - runAsNonRoot
    print("\n8. Que fait la directive securityContext.runAsNonRoot: true ?")
    print("a) Empêche l'exécution  b) Force l'exécution en tant qu'utilisateur non-root")
    print("c) Change le propriétaire  d) Chiffre les données")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Force l'exécution avec un utilisateur non-root pour la sécurité")

    # Question 9 - Network Policies
    print("\n9. Les Network Policies contrôlent :")
    print("a) L'authentification  b) Le trafic réseau entre pods")
    print("c) L'utilisation CPU  d) Le stockage")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Network Policies filtrent le trafic réseau au niveau L3/L4")

    # Question 10 - Ingress vs Egress
    print("\n10. Dans une Network Policy, Ingress et Egress contrôlent :")
    print("a) Entrée et sortie du trafic  b) Chiffrement et déchiffrement")
    print("c) Lecture et écriture  d) Production et développement")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Ingress=trafic entrant, Egress=trafic sortant")

    # Question 11 - Default deny
    print("\n11. Une politique 'default deny' en Network Policy :")
    print("a) Autorise tout  b) Bloque tout par défaut  c) Ignore les règles  d) Audit seulement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Bloque tout trafic non explicitement autorisé")

    # Question 12 - Capabilities
    print("\n12. Les capabilities Linux dans Kubernetes permettent :")
    print("a) Plus de mémoire  b) Privilèges spécifiques sans root complet")
    print("c) Réseau plus rapide  d) Stockage illimité")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Capabilities accordent des privilèges spécifiques sans être root")

    # Question 13 - readOnlyRootFilesystem
    print("\n13. readOnlyRootFilesystem: true améliore la sécurité en :")
    print("a) Chiffrant les données  b) Empêchant les modifications du système de fichiers")
    print("c) Accélérant les lectures  d) Compressant les fichiers")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Empêche les modifications malveillantes du système de fichiers")

    # Question 14 - Secrets
    print("\n14. Les Secrets Kubernetes stockent :")
    print("a) Configuration publique  b) Données sensibles encodées")
    print("c) Images Docker  d) Logs d'application")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Secrets stockent des données sensibles encodées en base64")

    # Question 15 - automountServiceAccountToken
    print("\n15. automountServiceAccountToken: false empêche :")
    print("a) Le démarrage du pod  b) Le montage automatique du token SA")
    print("c) L'accès réseau  d) L'utilisation de volumes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Empêche le montage automatique du token ServiceAccount")

    # Question 16 - allowPrivilegeEscalation
    print("\n16. allowPrivilegeEscalation: false empêche :")
    print("a) L'accès réseau  b) L'escalade de privilèges via setuid/setgid")
    print("c) L'utilisation de volumes  d) Les connexions TLS")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Empêche l'escalade de privilèges via les binaires setuid/setgid")

    # Question 17 - kubectl auth
    print("\n17. Comment tester les permissions RBAC d'un utilisateur ?")
    print("a) kubectl test  b) kubectl auth can-i  c) kubectl check  d) kubectl verify")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) kubectl auth can-i teste les permissions RBAC")

    # Question 18 - Namespace isolation
    print("\n18. Les namespaces Kubernetes fournissent :")
    print("a) Isolation réseau complète  b) Isolation logique des ressources")
    print("c) Chiffrement automatique  d) Backup automatique")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Namespaces fournissent une isolation logique, pas physique")

    # Question 19 - Security Context
    print("\n19. Un Security Context peut être défini au niveau :")
    print("a) Pod seulement  b) Container seulement  c) Pod et Container  d) Namespace seulement")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Security Context peut être défini au niveau Pod et Container")

    # Question 20 - Admission Controllers
    print("\n20. Les Admission Controllers dans Kubernetes :")
    print("a) Gèrent les utilisateurs  b) Valident/modifient les requêtes API")
    print("c) Stockent les données  d) Routent le trafic")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Admission Controllers interceptent et valident/modifient les requêtes API")

    # Question 21 - PodSecurityPolicy
    print("\n21. PodSecurityPolicy (PSP) est remplacé par :")
    print("a) NetworkPolicy  b) Pod Security Standards  c) RBAC  d) ServiceMesh")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Pod Security Standards remplacent les PodSecurityPolicy")

    # Question 22 - Resource Quotas
    print("\n22. Les Resource Quotas limitent :")
    print("a) Le trafic réseau  b) L'utilisation des ressources par namespace")
    print("c) Les connexions externes  d) Les images Docker")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Resource Quotas limitent l'utilisation des ressources par namespace")

    # Question 23 - TLS
    print("\n23. Dans Kubernetes, TLS est utilisé pour :")
    print("a) Compression  b) Chiffrement des communications")
    print("c) Load balancing  d) Monitoring")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) TLS chiffre les communications entre composants")

    # Question 24 - CIS Benchmarks
    print("\n24. Les CIS Benchmarks pour Kubernetes fournissent :")
    print("a) Performance metrics  b) Recommandations de sécurité")
    print("c) Configuration réseau  d) Gestion des images")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) CIS Benchmarks fournissent des recommandations de sécurité")

    # Question 25 - Audit Logging
    print("\n25. L'audit logging Kubernetes enregistre :")
    print("a) Performance des pods  b) Requêtes à l'API Server")
    print("c) Utilisation réseau  d) Erreurs d'application")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Audit logging enregistre toutes les requêtes à l'API Server")

    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les concepts de sécurité et RBAC Kubernetes")
        print("Vous pouvez passer au Quiz 2 - Helm Charts et GitOps")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Concepts RBAC de base (Roles, RoleBindings, ServiceAccounts)")
            print("- Pod Security Standards et Security Context")
        elif score < 15:
            print("- Network Policies et isolation réseau")
            print("- Gestion des secrets et configurations sécurisées")
        else:
            print("- Concepts avancés de sécurité Kubernetes")
            print("- Audit et monitoring de sécurité")
        print("Recommandation: Refaire les LABs 1-2 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Production - RBAC et Sécurité")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 3 - Kubernetes Production")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 2 - Helm Charts et GitOps")
    else:
        print("Direction: Révision LABs 1-2 et nouvelle tentative")
    print(f"{'='*60}")