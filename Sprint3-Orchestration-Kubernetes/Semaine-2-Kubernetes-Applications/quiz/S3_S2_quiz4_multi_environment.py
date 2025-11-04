#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz 4 - Kubernetes Applications - Multi-Environment
Sprint 3 - Semaine 2 - Séance 5

Couvre : Namespaces, Resource Quotas, Multi-tenancy, Configuration par environnement
"""

import random
import sys

class QuizKubernetesMultiEnvironment:
    def __init__(self):
        self.score = 0
        self.total_questions = 25
        self.seuil_validation = 0.72
        
    def run_quiz(self):
        print("🎯 QUIZ KUBERNETES MULTI-ENVIRONMENT")
        print("Sprint 3 - Semaine 2 - Séance 5")
        print("Couvre: Namespaces, Resource Quotas, Isolation, Configuration")
        
if __name__ == "__main__":
    quiz = QuizKubernetesMultiEnvironment()
    quiz.run_quiz()