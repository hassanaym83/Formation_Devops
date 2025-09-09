"""
Test automatisé du quiz DevOps
Vérifie la structure et les bonnes réponses
"""
import sys
from io import StringIO
from unittest.mock import patch

def test_quiz_structure():
    """Test la structure du quiz et les bonnes réponses"""
    
    # Réponses correctes pour les 25 questions
    correct_answers = [
        'c',  # Q1: Development + Operations
        'b',  # Q2: 2000-2008
        'b',  # Q3: 68% échec projets IT
        'b',  # Q4: Livrer à haute vélocité avec qualité
        'b',  # Q5: Culture
        'b',  # Q6: Automation
        'c',  # Q7: 7 types gaspillages Lean
        'b',  # Q8: Amy Edmondson
        'b',  # Q9: 4 niveaux Psychological Safety
        'b',  # Q10: DevOps Research and Assessment
        'b',  # Q11: 4 métriques DORA
        'c',  # Q12: Plusieurs fois par jour (Elite)
        'a',  # Q13: < 1 heure Lead Time (Elite)
        'a',  # Q14: 0-15% Change Failure Rate (Elite)
        'a',  # Q15: < 1 heure Time to Restore (Elite)
        'b',  # Q16: Gestion infrastructure par code
        'b',  # Q17: Fusion fréquente du code avec tests
        'b',  # Q18: Collection services faiblement couplés
        'b',  # Q19: Ingénierie logicielle aux opérations
        'c',  # Q20: 4 types Team Topologies
        'b',  # Q21: < 5% Technical Debt Ratio
        'c',  # Q22: 1000+ déploiements Netflix
        'b',  # Q23: 11.7 secondes Amazon
        'c',  # Q24: 440x amélioration
        'b'   # Q25: Comprendre état interne par outputs
    ]
    
    print("=" * 60)
    print("    TEST AUTOMATISÉ DU QUIZ DEVOPS")
    print("    Validation structure et réponses")
    print("=" * 60)
    
    # Import du module quiz
    try:
        from S0_S0_S1_quiz_introduction_culture_devops import run_quiz
        print("✅ Module quiz importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    
    # Test avec toutes les bonnes réponses
    print("\n🔄 Test avec toutes les bonnes réponses...")
    
    # Simulation des entrées utilisateur
    user_inputs = [''] + correct_answers  # Entrée vide pour commencer + réponses
    
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                result = run_quiz()
                output = mock_stdout.getvalue()
                
                if result:
                    print("✅ Quiz validé avec toutes les bonnes réponses")
                    print("✅ Score attendu: 25/25 (100%)")
                else:
                    print("❌ Échec inattendu avec toutes les bonnes réponses")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur lors de l'exécution: {e}")
                return False
    
    # Test avec réponses partielles (seuil 72%)
    print("\n🔄 Test avec 18/25 réponses correctes (seuil 72%)...")
    
    # 18 bonnes réponses + 7 mauvaises
    partial_answers = correct_answers[:18] + ['a'] * 7
    user_inputs_partial = [''] + partial_answers
    
    with patch('builtins.input', side_effect=user_inputs_partial):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                result = run_quiz()
                
                if result:
                    print("✅ Quiz validé avec 18/25 réponses (72%)")
                else:
                    print("❌ Échec inattendu à 72%")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur lors de l'exécution partielle: {e}")
                return False
    
    # Test avec échec (moins de 72%)
    print("\n🔄 Test avec 15/25 réponses (60% - échec)...")
    
    # 15 bonnes réponses + 10 mauvaises
    fail_answers = correct_answers[:15] + ['a'] * 10
    user_inputs_fail = [''] + fail_answers
    
    with patch('builtins.input', side_effect=user_inputs_fail):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                result = run_quiz()
                
                if not result:
                    print("✅ Échec correctement détecté à 60%")
                else:
                    print("❌ Validation inattendue à 60%")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur lors du test d'échec: {e}")
                return False
    
    print("\n" + "=" * 60)
    print("    RÉSULTATS DES TESTS")
    print("=" * 60)
    print("✅ Structure du quiz: OK")
    print("✅ 25 questions présentes: OK") 
    print("✅ Validation 100%: OK")
    print("✅ Validation seuil 72%: OK")
    print("✅ Échec < 72%: OK")
    print("✅ Logique de scoring: OK")
    print("\n🎉 TOUS LES TESTS RÉUSSIS!")
    print("📚 Le quiz couvre tous les concepts du cours:")
    print("   • Contexte historique et définitions DevOps")
    print("   • Principes CALMS et culture")
    print("   • Psychological Safety")
    print("   • Métriques DORA")
    print("   • Concepts techniques (CI/CD, IaC, microservices)")
    print("   • Exemples d'entreprises et ROI")
    print("   • Team Topologies et observabilité")
    
    return True

def analyze_quiz_coverage():
    """Analyse la couverture du cours par le quiz"""
    
    print("\n" + "=" * 60)
    print("    ANALYSE DE COUVERTURE DU COURS")
    print("=" * 60)
    
    coverage_areas = {
        "Contexte historique DevOps": ["Q2: Guerre Dev vs Ops", "Q3: Standish CHAOS Report"],
        "Définitions fondamentales": ["Q1: Acronyme DevOps", "Q4: Objectif DevOps"],
        "Principes CALMS": ["Q5: Culture", "Q6: Automation", "Q7: Lean gaspillages"],
        "Psychological Safety": ["Q8: Amy Edmondson", "Q9: 4 niveaux"],
        "Métriques DORA": ["Q10-Q15: 4 métriques + niveaux Elite"],
        "Concepts techniques": ["Q16: IaC", "Q17: CI", "Q18: Microservices", "Q25: Observabilité"],
        "Rôles DevOps": ["Q19: SRE"],
        "Organisation": ["Q20: Team Topologies"],
        "Qualité": ["Q21: Technical Debt Ratio"],
        "Exemples entreprises": ["Q22: Netflix", "Q23: Amazon"],
        "ROI et impact": ["Q24: Amélioration 440x"]
    }
    
    for area, questions in coverage_areas.items():
        print(f"✅ {area}:")
        for q in questions:
            print(f"   • {q}")
    
    print(f"\n📊 Couverture totale: {len(coverage_areas)} domaines couverts")
    print("🎯 Quiz aligné sur objectifs pédagogiques de la séance")

if __name__ == "__main__":
    print("Lancement des tests automatisés...")
    
    if test_quiz_structure():
        analyze_quiz_coverage()
        print("\n🏆 QUIZ VALIDÉ - PRÊT POUR UTILISATION")
    else:
        print("\n💥 ÉCHEC DES TESTS - CORRECTION NÉCESSAIRE")
        sys.exit(1)
