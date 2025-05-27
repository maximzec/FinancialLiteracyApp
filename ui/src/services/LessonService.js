import ApiService from './ApiService';
import GamificationService from './GamificationService';
import AIService from './AIService';

export const LessonService = {
    // Получение урока по ID
    async getLesson(id) {
        try {
            console.log(`[Lessons] Получение урока ${id}`);

            const response = await ApiService.get(`/lessons/${id}`);

            // Получаем прогресс пользователя для урока
            const progress = await this.getLessonProgress(id);

            return {
                ...response,
                user_progress: progress
            };
        } catch (error) {
            console.error('[Lessons] Ошибка получения урока:', error);
            throw error;
        }
    },

    // Получение списка всех уроков
    async getLessons(filters = {}) {
        try {
            console.log('[Lessons] Получение списка уроков');

            const response = await ApiService.get('/lessons', filters);
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения списка уроков:', error);
            throw error;
        }
    },

    // Начало прохождения урока
    async startLesson(lessonId) {
        try {
            console.log(`[Lessons] Начало урока ${lessonId}`);

            const response = await ApiService.post(`/lessons/${lessonId}/start`);

            // Создаем локальную запись о прогрессе для отслеживания
            const progressData = {
                lesson_id: lessonId,
                status: 'in_progress',
                progress_percentage: 0,
                time_spent_minutes: 0,
                started_at: new Date().toISOString()
            };

            localStorage.setItem(`lesson_progress_${lessonId}`, JSON.stringify(progressData));

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка начала урока:', error);
            throw error;
        }
    },

    // Обновление прогресса урока
    async updateLessonProgress(lessonId, progressData) {
        try {
            console.log(`[Lessons] Обновление прогресса урока ${lessonId}:`, progressData);

            const response = await ApiService.put(`/lessons/${lessonId}/progress`, progressData);

            // Обновляем локальный прогресс
            const currentProgress = this.getLessonProgressLocal(lessonId);
            const updatedProgress = {
                ...currentProgress,
                ...progressData,
                updated_at: new Date().toISOString()
            };

            localStorage.setItem(`lesson_progress_${lessonId}`, JSON.stringify(updatedProgress));

            // Если урок завершен, начисляем коины
            if (progressData.status === 'completed' && currentProgress.status !== 'completed') {
                try {
                    await GamificationService.addCoins(25, `Завершение урока`);
                } catch (gamificationError) {
                    console.warn('[Lessons] Не удалось начислить коины:', gamificationError);
                }

                // Обновляем прогресс персонального плана
                try {
                    await AIService.updatePlanProgress(currentProgress.current_step + 1);
                } catch (aiError) {
                    console.warn('[Lessons] Не удалось обновить AI план:', aiError);
                }
            }

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка обновления прогресса:', error);
            throw error;
        }
    },

    // Получение прогресса урока
    async getLessonProgress(lessonId) {
        try {
            console.log(`[Lessons] Получение прогресса урока ${lessonId}`);

            const response = await ApiService.get(`/lessons/${lessonId}/progress`);
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения прогресса:', error);
            // Возвращаем локальный прогресс в случае ошибки
            return this.getLessonProgressLocal(lessonId);
        }
    },

    // Получение локального прогресса
    getLessonProgressLocal(lessonId) {
        const saved = localStorage.getItem(`lesson_progress_${lessonId}`);
        return saved ? JSON.parse(saved) : {
            lesson_id: lessonId,
            status: 'not_started',
            progress_percentage: 0,
            time_spent_minutes: 0,
            started_at: null,
            completed_at: null
        };
    },

    // Получение тестов урока
    async getLessonQuizzes(lessonId) {
        try {
            console.log(`[Lessons] Получение тестов урока ${lessonId}`);

            const response = await ApiService.get(`/lessons/${lessonId}/quiz`);
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения тестов:', error);
            throw error;
        }
    },

    // Отправка ответа на тест с AI валидацией
    async submitQuizAnswer(quizId, answerData) {
        try {
            console.log(`[Lessons] Отправка ответа на тест ${quizId}:`, answerData);

            const response = await ApiService.post(`/lessons/quiz/${quizId}/answer`, {
                user_answer: answerData.userAnswer,
                answer_index: answerData.answerIndex
            });

            // Используем AI для дополнительной валидации ответа
            try {
                const aiValidation = await AIService.validateQuizAnswer(quizId, answerData.userAnswer);
                response.ai_validation = aiValidation;
            } catch (aiError) {
                console.warn('[Lessons] AI валидация недоступна:', aiError);
            }

            // Начисляем коины за правильный ответ
            if (response.is_correct) {
                try {
                    await GamificationService.addCoins(10, 'Правильный ответ на тест');
                } catch (gamificationError) {
                    console.warn('[Lessons] Не удалось начислить коины:', gamificationError);
                }
            }

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка отправки ответа:', error);
            throw error;
        }
    },

    // Отметить урок как завершенный
    async completeLesson(lessonId) {
        try {
            console.log(`[Lessons] Завершение урока ${lessonId}`);

            const response = await ApiService.post(`/lessons/${lessonId}/complete`);

            // Обновляем локальный прогресс
            await this.updateLessonProgress(lessonId, {
                status: 'completed',
                progress_percentage: 100,
                completed_at: new Date().toISOString()
            });

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка завершения урока:', error);
            throw error;
        }
    },

    // Получение статистики обучения пользователя
    async getLearningStats() {
        try {
            console.log('[Lessons] Получение статистики обучения');

            const response = await ApiService.get('/users/learning-stats');
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения статистики:', error);
            throw error;
        }
    },

    // Получение рекомендуемых уроков
    async getRecommendedLessons(limit = 3) {
        try {
            console.log('[Lessons] Получение рекомендуемых уроков');

            const response = await ApiService.get('/lessons/recommended', { limit });

            // Дополняем AI рекомендациями если доступно
            try {
                const aiRecommendations = await AIService.getRecommendations(limit);
                const lessonRecommendations = aiRecommendations
                    .filter(rec => rec.content_type === 'lesson')
                    .map(rec => ({
                        ...rec,
                        recommendation_reason: rec.reason,
                        confidence: rec.confidence
                    }));

                // Объединяем рекомендации с backend и AI
                response.ai_recommendations = lessonRecommendations;
            } catch (aiError) {
                console.warn('[Lessons] AI рекомендации недоступны:', aiError);
            }

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения рекомендаций:', error);
            throw error;
        }
    },

    // Поиск уроков
    async searchLessons(query, filters = {}) {
        try {
            console.log('[Lessons] Поиск уроков:', query);

            const response = await ApiService.get('/lessons/search', {
                query: query,
                ...filters
            });

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка поиска уроков:', error);
            throw error;
        }
    },

    // Получение категорий уроков
    async getLessonCategories() {
        try {
            console.log('[Lessons] Получение категорий уроков');

            const response = await ApiService.get('/lessons/categories');
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения категорий:', error);
            throw error;
        }
    },

    // Генерация адаптивного контента урока с помощью AI
    async generateAdaptiveContent(lessonId, contentType = 'explanation') {
        try {
            console.log(`[Lessons] Генерация адаптивного контента для урока ${lessonId}`);

            const aiContent = await AIService.generateLessonContent(lessonId, contentType);

            return {
                success: true,
                content: aiContent
            };
        } catch (error) {
            console.error('[Lessons] Ошибка генерации контента:', error);
            return {
                success: false,
                error: error.message
            };
        }
    },

    // Получение шагов урока
    async getLessonSteps(lessonId) {
        try {
            console.log(`[Lessons] Получение шагов урока ${lessonId}`);

            const response = await ApiService.get(`/lessons/${lessonId}/steps`);
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения шагов урока:', error);
            throw error;
        }
    },

    // Отметить шаг урока как завершенный
    async completeStep(lessonId, stepId) {
        try {
            console.log(`[Lessons] Завершение шага ${stepId} урока ${lessonId}`);

            const response = await ApiService.post(`/lessons/${lessonId}/steps/${stepId}/complete`);
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка завершения шага:', error);
            throw error;
        }
    },

    // Получение материалов урока
    async getLessonMaterials(lessonId) {
        try {
            console.log(`[Lessons] Получение материалов урока ${lessonId}`);

            const response = await ApiService.get(`/lessons/${lessonId}/materials`);
            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка получения материалов:', error);
            throw error;
        }
    },

    // Оценка урока
    async rateLesson(lessonId, rating, comment = '') {
        try {
            console.log(`[Lessons] Оценка урока ${lessonId}: ${rating}`);

            const response = await ApiService.post(`/lessons/${lessonId}/rate`, {
                rating: rating,
                comment: comment
            });

            return response;
        } catch (error) {
            console.error('[Lessons] Ошибка оценки урока:', error);
            throw error;
        }
    }
}; 