import ApiService from './ApiService';
import AuthService from './AuthService';

// Сервис управления пользователями и профилями
class UserService {
    constructor() {
        this.userPreferences = this.loadPreferences();
    }

    // Загрузка настроек пользователя
    loadPreferences() {
        const saved = localStorage.getItem('user_preferences');
        return saved ? JSON.parse(saved) : {
            notifications: {
                email_lessons: true,
                email_challenges: true,
                push_reminders: true,
                weekly_reports: true
            },
            learning: {
                preferred_style: 'visual',
                difficulty_level: 'beginner',
                daily_goal_minutes: 30,
                reminder_time: '18:00'
            },
            privacy: {
                profile_visibility: 'private',
                show_in_leaderboard: true,
                data_analytics: true
            }
        };
    }

    // Сохранение настроек
    savePreferences() {
        localStorage.setItem('user_preferences', JSON.stringify(this.userPreferences));
    }

    // Получение профиля текущего пользователя
    async getCurrentUserProfile() {
        try {
            console.log('[User] Получение профиля текущего пользователя');

            const response = await ApiService.get('/users/me');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения профиля:', error);
            throw error;
        }
    }

    // Создание профиля пользователя
    async createUserProfile(profileData) {
        try {
            console.log('[User] Создание профиля пользователя:', profileData);

            const response = await ApiService.post('/users/profile', {
                age: profileData.age,
                financial_experience: profileData.financialExperience,
                monthly_income: profileData.monthlyIncome,
                financial_goals: profileData.financialGoals,
                risk_tolerance: profileData.riskTolerance,
                preferred_learning_style: profileData.preferredLearningStyle,
                goals: profileData.goals
            });

            // Обновляем профиль через AuthService
            await AuthService.updateProfile(profileData);

            return response;
        } catch (error) {
            console.error('[User] Ошибка создания профиля:', error);
            throw error;
        }
    }

    // Обновление профиля пользователя
    async updateUserProfile(profileData) {
        try {
            console.log('[User] Обновление профиля пользователя:', profileData);

            const response = await ApiService.put('/users/profile', profileData);

            // Обновляем профиль через AuthService
            await AuthService.updateProfile(profileData);

            return response;
        } catch (error) {
            console.error('[User] Ошибка обновления профиля:', error);
            throw error;
        }
    }

    // Получение профиля пользователя
    async getUserProfile() {
        try {
            console.log('[User] Получение профиля пользователя');

            const response = await ApiService.get('/users/profile');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения профиля:', error);
            throw error;
        }
    }

    // Удаление профиля пользователя
    async deleteUserProfile() {
        try {
            console.log('[User] Удаление профиля пользователя');

            const response = await ApiService.delete('/users/profile');
            return response;
        } catch (error) {
            console.error('[User] Ошибка удаления профиля:', error);
            throw error;
        }
    }

    // Получение статистики обучения пользователя
    async getUserLearningStats() {
        try {
            console.log('[User] Получение статистики обучения');

            const response = await ApiService.get('/users/learning-stats');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения статистики:', error);
            throw error;
        }
    }

    // Получение дашборда пользователя
    async getUserDashboard() {
        try {
            console.log('[User] Получение дашборда пользователя');

            const response = await ApiService.get('/users/dashboard');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения дашборда:', error);
            throw error;
        }
    }

    // Получение достижений пользователя
    async getUserAchievements() {
        try {
            console.log('[User] Получение достижений пользователя');

            const response = await ApiService.get('/users/achievements');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения достижений:', error);
            throw error;
        }
    }

    // Получение настроек пользователя
    async getUserPreferences() {
        try {
            console.log('[User] Получение настроек пользователя');

            const response = await ApiService.get('/users/preferences');

            // Обновляем локальные настройки
            this.userPreferences = { ...this.userPreferences, ...response };
            this.savePreferences();

            return this.userPreferences;
        } catch (error) {
            console.error('[User] Ошибка получения настроек:', error);
            return this.userPreferences;
        }
    }

    // Обновление настроек пользователя
    async updateUserPreferences(preferences) {
        try {
            console.log('[User] Обновление настроек пользователя:', preferences);

            const response = await ApiService.put('/users/preferences', preferences);

            // Обновляем локальные настройки
            this.userPreferences = {
                ...this.userPreferences,
                ...preferences
            };

            this.savePreferences();

            return response;
        } catch (error) {
            console.error('[User] Ошибка обновления настроек:', error);
            throw error;
        }
    }

    // Удаление аккаунта пользователя
    async deleteUserAccount(confirmation) {
        try {
            if (confirmation !== 'DELETE_MY_ACCOUNT') {
                throw new Error('Неверное подтверждение удаления');
            }

            console.log('[User] Удаление аккаунта пользователя');

            const response = await ApiService.delete('/users/account', {
                confirmation: confirmation
            });

            // Выходим из системы
            await AuthService.logout();

            // Очищаем все локальные данные
            localStorage.clear();

            return response;
        } catch (error) {
            console.error('[User] Ошибка удаления аккаунта:', error);
            throw error;
        }
    }

    // Экспорт данных пользователя
    async exportUserData() {
        try {
            console.log('[User] Экспорт данных пользователя');

            const response = await ApiService.get('/users/export');

            // Создаем файл для скачивания
            const dataStr = JSON.stringify(response, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);

            const link = document.createElement('a');
            link.href = url;
            link.download = `financial_app_data_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);

            return {
                success: true,
                message: 'Данные успешно экспортированы'
            };
        } catch (error) {
            console.error('[User] Ошибка экспорта данных:', error);
            throw error;
        }
    }

    // Получение активности пользователя
    async getUserActivity(period = 'week', limit = 20) {
        try {
            console.log(`[User] Получение активности за ${period}`);

            const response = await ApiService.get('/users/activity', {
                period: period,
                limit: limit
            });

            return response;
        } catch (error) {
            console.error('[User] Ошибка получения активности:', error);
            throw error;
        }
    }

    // Получение уведомлений пользователя
    async getUserNotifications(unread_only = false, limit = 10) {
        try {
            console.log('[User] Получение уведомлений');

            const response = await ApiService.get('/users/notifications', {
                unread_only: unread_only,
                limit: limit
            });

            return response;
        } catch (error) {
            console.error('[User] Ошибка получения уведомлений:', error);
            throw error;
        }
    }

    // Отметить уведомление как прочитанное
    async markNotificationAsRead(notificationId) {
        try {
            console.log(`[User] Отметка уведомления ${notificationId} как прочитанного`);

            const response = await ApiService.put(`/users/notifications/${notificationId}/read`);
            return response;
        } catch (error) {
            console.error('[User] Ошибка отметки уведомления:', error);
            throw error;
        }
    }

    // Получение рекомендаций для пользователя
    async getUserRecommendations(type = 'all', limit = 5) {
        try {
            console.log(`[User] Получение рекомендаций типа ${type}`);

            const response = await ApiService.get('/users/recommendations', {
                type: type,
                limit: limit
            });

            return response;
        } catch (error) {
            console.error('[User] Ошибка получения рекомендаций:', error);
            throw error;
        }
    }

    // Получение прогресса пользователя
    async getUserProgress() {
        try {
            console.log('[User] Получение прогресса пользователя');

            const response = await ApiService.get('/users/progress');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения прогресса:', error);
            throw error;
        }
    }

    // Обновление целей пользователя
    async updateUserGoals(goals) {
        try {
            console.log('[User] Обновление целей пользователя:', goals);

            const response = await ApiService.put('/users/goals', { goals });
            return response;
        } catch (error) {
            console.error('[User] Ошибка обновления целей:', error);
            throw error;
        }
    }

    // Получение истории обучения
    async getLearningHistory(limit = 50) {
        try {
            console.log('[User] Получение истории обучения');

            const response = await ApiService.get('/users/learning-history', { limit });
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения истории обучения:', error);
            throw error;
        }
    }

    // Получение сертификатов пользователя
    async getUserCertificates() {
        try {
            console.log('[User] Получение сертификатов пользователя');

            const response = await ApiService.get('/users/certificates');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения сертификатов:', error);
            throw error;
        }
    }

    // Создание заявки на сертификат
    async requestCertificate(courseId) {
        try {
            console.log(`[User] Создание заявки на сертификат для курса ${courseId}`);

            const response = await ApiService.post('/users/certificates/request', {
                course_id: courseId
            });

            return response;
        } catch (error) {
            console.error('[User] Ошибка создания заявки на сертификат:', error);
            throw error;
        }
    }

    // Получение социальных связей
    async getSocialConnections() {
        try {
            console.log('[User] Получение социальных связей');

            const response = await ApiService.get('/users/social-connections');
            return response;
        } catch (error) {
            console.error('[User] Ошибка получения социальных связей:', error);
            throw error;
        }
    }

    // Добавление друга
    async addFriend(userId) {
        try {
            console.log(`[User] Добавление друга ${userId}`);

            const response = await ApiService.post('/users/friends/add', {
                friend_user_id: userId
            });

            return response;
        } catch (error) {
            console.error('[User] Ошибка добавления друга:', error);
            throw error;
        }
    }

    // Удаление друга
    async removeFriend(userId) {
        try {
            console.log(`[User] Удаление друга ${userId}`);

            const response = await ApiService.delete(`/users/friends/${userId}`);
            return response;
        } catch (error) {
            console.error('[User] Ошибка удаления друга:', error);
            throw error;
        }
    }
}

export default new UserService(); 