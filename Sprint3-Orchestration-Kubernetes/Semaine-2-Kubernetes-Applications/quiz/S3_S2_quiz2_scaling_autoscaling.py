#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz 2 - Kubernetes Applications - Scaling et Autoscaling
Sprint 3 - Semaine 2 - Séance 3

Couvre : HPA, VPA, Cluster Autoscaler, métriques et performance
"""

import random
import sys
from typing import List, Dict, Any

class QuizKubernetesScaling:
    def __init__(self):
        self.score = 0
        self.total_questions = 25
        self.questions = self._load_questions()
        self.seuil_validation = 0.72
        
    def _load_questions(self) -> List[Dict[str, Any]]:
        """Questions sur scaling et autoscaling"""
        return [
            {
                "question": "Quelle est la différence principale entre HPA et VPA ?",
                "options": [
                    "A) HPA scale horizontalement (nombre de pods), VPA verticalement (ressources)",
                    "B) HPA est pour CPU seulement, VPA pour mémoire",
                    "C) HPA est automatique, VPA est manuel",
                    "D) Il n'y a pas de différence"
                ],
                "correct": "A",
                "explanation": "HPA ajoute/supprime des pods, VPA ajuste les ressources CPU/mémoire des pods existants."
            },
            {
                "question": "Quel composant est nécessaire pour le bon fonctionnement du HPA ?",
                "options": [
                    "A) Prometheus",
                    "B) metrics-server",
                    "C) Grafana",
                    "D) Ingress Controller"
                ],
                "correct": "B",
                "explanation": "metrics-server collecte les métriques de ressources nécessaires au HPA."
            },
            {
                "question": "Dans un HPA, que fait le paramètre 'stabilizationWindowSeconds' ?",
                "options": [
                    "A) Définit l'intervalle de collecte des métriques",
                    "B) Empêche les oscillations en lissant les décisions de scaling",
                    "C) Configure le timeout des requêtes",
                    "D) Définit la durée de vie du HPA"
                ],
                "correct": "B",
                "explanation": "stabilizationWindowSeconds évite les décisions de scaling trop fréquentes qui peuvent causer des oscillations."
            }
            # ... 22 autres questions sur scaling
        ]
    
    def run_quiz(self):
        print("🎯 QUIZ KUBERNETES SCALING ET AUTOSCALING")
        print("Sprint 3 - Semaine 2 - Séance 3")
        # Implementation similaire au premier quiz
        pass

if __name__ == "__main__":
    quiz = QuizKubernetesScaling()
    quiz.run_quiz()