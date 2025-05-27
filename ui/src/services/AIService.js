import ApiService from './ApiService';

// Сервис AI и машинного обучения
class AIService {
    constructor() {
        this.personalPlan = null;
        this.aiInteractions = [];
        this.recommendations = [];
    }

    // Создание персонального плана обучения
    async createPersonalPlan(planData) {
        try {
            console.log('[AI] Создание персонального плана обучения:', planData);

            const response = await ApiService.post('/ai/personal-plan', {
                goals: planData.goals,
                experience_level: planData.experienceLevel,
                preferences: planData.preferences,
                time_commitment_hours: planData.timeCommitmentHours
            });

            this.personalPlan = response;
            localStorage.setItem('personal_plan', JSON.stringify(response));

            return response;
        } catch (error) {
            console.error('[AI] Ошибка создания персонального плана:', error);
            throw error;
        }
    }

    // Получение персонального плана
    async getPersonalPlan() {
        try {
            console.log('[AI] Получение персонального плана');

            const response = await ApiService.get('/ai/personal-plan');

            this.personalPlan = response;
            if (response) {
                localStorage.setItem('personal_plan', JSON.stringify(response));
            }

            return response;
        } catch (error) {
            console.error('[AI] Ошибка получения плана:', error);
            // Возвращаем локально сохраненный план в случае ошибки
            const savedPlan = localStorage.getItem('personal_plan');
            if (savedPlan) {
                this.personalPlan = JSON.parse(savedPlan);
                return this.personalPlan;
            }
            return null;
        }
    }

    // Генерация адаптивного контента урока
    async generateLessonContent(lessonId, contentType = 'explanation') {
        try {
            console.log(`[AI] Генерация контента для урока ${lessonId}, тип: ${contentType}`);

            const response = await ApiService.post('/ai/lesson-content', {
                lesson_id: lessonId,
                content_type: contentType,
                personalization_level: 'adaptive'
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка генерации контента:', error);
            throw error;
        }
    }

    // Интеллектуальная валидация ответов на тесты
    async validateQuizAnswer(quizId, userAnswer) {
        try {
            console.log(`[AI] Валидация ответа на тест ${quizId}:`, userAnswer);

            const response = await ApiService.post('/ai/quiz-validation', {
                quiz_id: quizId,
                user_answer: userAnswer
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка валидации ответа:', error);
            throw error;
        }
    }

    // AI-тьютор для ответов на вопросы
    async askTutor(question, context = null) {
        try {
            console.log('[AI] Вопрос к AI-тьютору:', question);

            const response = await ApiService.post('/ai/tutor-chat', {
                question: question,
                context: context
            });

            // Сохраняем взаимодействие локально
            this.aiInteractions.push({
                id: Date.now(),
                question: question,
                response: response.response_text,
                timestamp: new Date().toISOString()
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка AI-тьютора:', error);
            throw error;
        }
    }

    // Получение персонализированных рекомендаций
    async getRecommendations(limit = 5) {
        try {
            console.log('[AI] Получение персонализированных рекомендаций');

            const response = await ApiService.get('/ai/recommendations', { limit });

            this.recommendations = response;
            return response;
        } catch (error) {
            console.error('[AI] Ошибка получения рекомендаций:', error);
            throw error;
        }
    }

    // Генерация финансовых концепций
    async generateFinancialConcepts(category, difficultyLevel, count = 10) {
        try {
            console.log(`[AI] Генерация ${count} концепций категории ${category}, уровень ${difficultyLevel}`);

            const response = await ApiService.post('/ai/generate-concepts', {
                category: category,
                difficulty_level: difficultyLevel,
                count: count
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка генерации концепций:', error);
            throw error;
        }
    }

    // Анализ качества контента
    async analyzeContent(content, contentType = 'lesson') {
        try {
            console.log('[AI] Анализ качества контента');

            const response = await ApiService.post('/ai/analyze-content', {
                content: content,
                content_type: contentType
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка анализа контента:', error);
            throw error;
        }
    }

    // Получение истории взаимодействий с AI
    async getAIInteractions(interactionType = null, limit = 20) {
        try {
            console.log('[AI] Получение истории взаимодействий с AI');

            const params = { limit };
            if (interactionType) {
                params.interaction_type = interactionType;
            }

            const response = await ApiService.get('/ai/interactions', params);
            return response;
        } catch (error) {
            console.error('[AI] Ошибка получения взаимодействий:', error);
            // Возвращаем локальные взаимодействия в случае ошибки
            return this.aiInteractions.slice(-limit);
        }
    }

    // Обновление прогресса персонального плана
    async updatePlanProgress(stepNumber) {
        try {
            console.log(`[AI] Обновление прогресса плана: шаг ${stepNumber}`);

            const response = await ApiService.put('/ai/personal-plan/progress', {
                step_number: stepNumber
            });

            // Обновляем локальный план
            if (this.personalPlan) {
                this.personalPlan.current_step = stepNumber;
                this.personalPlan.completion_percentage = response.completion_percentage;
                this.personalPlan.updated_at = new Date().toISOString();
                localStorage.setItem('personal_plan', JSON.stringify(this.personalPlan));
            }

            return response;
        } catch (error) {
            console.error('[AI] Ошибка обновления прогресса:', error);
            throw error;
        }
    }

    // Получение AI инсайтов для пользователя
    async getUserInsights() {
        try {
            console.log('[AI] Получение AI инсайтов для пользователя');

            const response = await ApiService.get('/ai/user-insights');
            return response;
        } catch (error) {
            console.error('[AI] Ошибка получения инсайтов:', error);
            throw error;
        }
    }

    // Генерация персонализированного контента
    async generatePersonalizedContent(contentType, userPreferences) {
        try {
            console.log('[AI] Генерация персонализированного контента:', contentType);

            const response = await ApiService.post('/ai/personalized-content', {
                content_type: contentType,
                user_preferences: userPreferences
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка генерации персонализированного контента:', error);
            throw error;
        }
    }

    // Анализ прогресса обучения
    async analyzeLearningProgress(userId) {
        try {
            console.log('[AI] Анализ прогресса обучения');

            const response = await ApiService.get('/ai/learning-analysis');
            return response;
        } catch (error) {
            console.error('[AI] Ошибка анализа прогресса:', error);
            throw error;
        }
    }

    // Предсказание следующих действий пользователя
    async predictUserActions() {
        try {
            console.log('[AI] Предсказание следующих действий пользователя');

            const response = await ApiService.get('/ai/predict-actions');
            return response;
        } catch (error) {
            console.error('[AI] Ошибка предсказания действий:', error);
            throw error;
        }
    }

    // Оптимизация учебного плана
    async optimizeLearningPlan(currentPlan, userFeedback) {
        try {
            console.log('[AI] Оптимизация учебного плана');

            const response = await ApiService.post('/ai/optimize-plan', {
                current_plan: currentPlan,
                user_feedback: userFeedback
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка оптимизации плана:', error);
            throw error;
        }
    }

    // Генерация адаптивных вопросов
    async generateAdaptiveQuestions(topic, difficultyLevel, userKnowledge) {
        try {
            console.log('[AI] Генерация адаптивных вопросов');

            const response = await ApiService.post('/ai/adaptive-questions', {
                topic: topic,
                difficulty_level: difficultyLevel,
                user_knowledge: userKnowledge
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка генерации вопросов:', error);
            throw error;
        }
    }

    // Анализ эмоционального состояния по тексту
    async analyzeSentiment(text) {
        try {
            console.log('[AI] Анализ эмоционального состояния');

            const response = await ApiService.post('/ai/sentiment-analysis', {
                text: text
            });

            return response;
        } catch (error) {
            console.error('[AI] Ошибка анализа эмоций:', error);
            throw error;
        }
    }

    // Получение AI статистики
    async getAIStats() {
        try {
            console.log('[AI] Получение AI статистики');

            const response = await ApiService.get('/ai/stats');
            return response;
        } catch (error) {
            console.error('[AI] Ошибка получения AI статистики:', error);
            throw error;
        }
    }
}

export default new AIService(); 