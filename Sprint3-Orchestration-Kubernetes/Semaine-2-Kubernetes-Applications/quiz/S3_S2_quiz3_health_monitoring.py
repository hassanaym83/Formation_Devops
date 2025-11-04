#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz 3 - Kubernetes Applications - Health et Monitoring
Sprint 3 - Semaine 2 - Séance 4

Couvre : Health checks, Probes, Monitoring, Prometheus, Grafana
"""

import random
import sys

class QuizKubernetesHealthMonitoring:
    def __init__(self):
        self.score = 0
        self.total_questions = 25
        self.seuil_validation = 0.72
        
    def run_quiz(self):
        print("🎯 QUIZ KUBERNETES HEALTH ET MONITORING")
        print("Sprint 3 - Semaine 2 - Séance 4")
        print("Couvre: Health checks, Probes, Monitoring, Observabilité")
        
if __name__ == "__main__":
    quiz = QuizKubernetesHealthMonitoring()
    quiz.run_quiz()