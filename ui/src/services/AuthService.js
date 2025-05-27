import ApiService from './ApiService';

// Сервис авторизации
class AuthService {
    constructor() {
        this.user = this.loadUserFromStorage();
        this.token = localStorage.getItem('auth_token');

        // Устанавливаем токен в ApiService при инициализации
        if (this.token) {
            ApiService.setToken(this.token);
        }
    }

    // Загрузка пользователя из localStorage
    loadUserFromStorage() {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    }

    // Сохранение пользователя в localStorage
    saveUserToStorage(user, token) {
        localStorage.setItem('user_data', JSON.stringify(user));
        localStorage.setItem('auth_token', token);
        this.user = user;
        this.token = token;
        ApiService.setToken(token);
    }

    // Регистрация пользователя
    async register(userData) {
        try {
            console.log('[Auth] Регистрация пользователя:', userData);

            const response = await ApiService.post('/auth/register', {
                email: userData.email,
                password: userData.password,
                first_name: userData.firstName,
                last_name: userData.lastName,
                phone: userData.phone
            });

            // Сохраняем данные пользователя и токен
            this.saveUserToStorage(response.user, response.access_token);

            return {
                success: true,
                user: response.user,
                token: response.access_token
            };
        } catch (error) {
            console.error('[Auth] Ошибка регистрации:', error);
            throw error;
        }
    }

    // Авторизация пользователя
    async login(credentials) {
        try {
            console.log('[Auth] Авторизация пользователя:', credentials.email);

            const response = await ApiService.post('/auth/login', {
                email: credentials.email,
                password: credentials.password
            });

            // Сохраняем данные пользователя и токен
            this.saveUserToStorage(response.user, response.access_token);

            return {
                success: true,
                user: response.user,
                token: response.access_token
            };
        } catch (error) {
            console.error('[Auth] Ошибка авторизации:', error);
            throw error;
        }
    }

    // Выход из системы
    async logout() {
        try {
            console.log('[Auth] Выход из системы');

            // Отправляем запрос на backend для инвалидации токена
            if (this.token) {
                await ApiService.post('/auth/logout');
            }

            // Очищаем локальные данные
            this.user = null;
            this.token = null;
            localStorage.removeItem('user_data');
            localStorage.removeItem('auth_token');
            ApiService.removeToken();

            return { success: true };
        } catch (error) {
            console.error('[Auth] Ошибка выхода:', error);
            // Даже если запрос не удался, очищаем локальные данные
            this.user = null;
            this.token = null;
            localStorage.removeItem('user_data');
            localStorage.removeItem('auth_token');
            ApiService.removeToken();
            throw error;
        }
    }

    // Получение текущего пользователя
    getUser() {
        return this.user;
    }

    // Проверка авторизации
    isLoggedIn() {
        return !!(this.user && this.token);
    }

    // Проверка валидности токена
    isTokenValid() {
        if (!this.token) return false;

        try {
            // Простая проверка JWT токена (без верификации подписи)
            const payload = JSON.parse(atob(this.token.split('.')[1]));
            const currentTime = Date.now() / 1000;
            return payload.exp > currentTime;
        } catch (error) {
            console.error('[Auth] Ошибка проверки токена:', error);
            return false;
        }
    }

    // Обновление профиля пользователя
    async updateProfile(profileData) {
        try {
            console.log('[Auth] Обновление профиля:', profileData);

            const response = await ApiService.put('/auth/profile', profileData);

            // Обновляем локальные данные пользователя
            this.user = { ...this.user, ...response.user };
            localStorage.setItem('user_data', JSON.stringify(this.user));

            return {
                success: true,
                user: this.user
            };
        } catch (error) {
            console.error('[Auth] Ошибка обновления профиля:', error);
            throw error;
        }
    }

    // Смена пароля
    async changePassword(passwordData) {
        try {
            console.log('[Auth] Смена пароля');

            const response = await ApiService.post('/auth/change-password', {
                current_password: passwordData.currentPassword,
                new_password: passwordData.newPassword
            });

            return {
                success: true,
                message: response.message || 'Пароль успешно изменен'
            };
        } catch (error) {
            console.error('[Auth] Ошибка смены пароля:', error);
            throw error;
        }
    }

    // Восстановление пароля
    async resetPassword(email) {
        try {
            console.log('[Auth] Восстановление пароля для:', email);

            const response = await ApiService.post('/auth/reset-password', {
                email: email
            });

            return {
                success: true,
                message: response.message || 'Инструкции по восстановлению пароля отправлены на email'
            };
        } catch (error) {
            console.error('[Auth] Ошибка восстановления пароля:', error);
            throw error;
        }
    }

    // Подтверждение восстановления пароля
    async confirmPasswordReset(token, newPassword) {
        try {
            console.log('[Auth] Подтверждение восстановления пароля');

            const response = await ApiService.post('/auth/confirm-reset-password', {
                token: token,
                new_password: newPassword
            });

            return {
                success: true,
                message: response.message || 'Пароль успешно восстановлен'
            };
        } catch (error) {
            console.error('[Auth] Ошибка подтверждения восстановления:', error);
            throw error;
        }
    }

    // Обновление токена
    async refreshToken() {
        try {
            console.log('[Auth] Обновление токена');

            const response = await ApiService.post('/auth/refresh');

            // Обновляем токен
            this.token = response.access_token;
            localStorage.setItem('auth_token', this.token);
            ApiService.setToken(this.token);

            return {
                success: true,
                token: this.token
            };
        } catch (error) {
            console.error('[Auth] Ошибка обновления токена:', error);
            // При ошибке обновления токена выходим из системы
            await this.logout();
            throw error;
        }
    }

    // Получение информации о текущем пользователе с сервера
    async getCurrentUser() {
        try {
            console.log('[Auth] Получение текущего пользователя');

            const response = await ApiService.get('/auth/me');

            // Обновляем локальные данные
            this.user = response.user;
            localStorage.setItem('user_data', JSON.stringify(this.user));

            return this.user;
        } catch (error) {
            console.error('[Auth] Ошибка получения пользователя:', error);
            throw error;
        }
    }
}

export default new AuthService(); 