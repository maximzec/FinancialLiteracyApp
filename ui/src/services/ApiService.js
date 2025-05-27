// Базовый сервис для работы с API
class ApiService {
    constructor() {
        this.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1';
        this.token = localStorage.getItem('auth_token');
    }

    // Установка токена авторизации
    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('auth_token', token);
        } else {
            localStorage.removeItem('auth_token');
        }
    }

    // Удаление токена
    removeToken() {
        this.token = null;
        localStorage.removeItem('auth_token');
    }

    // Получение заголовков для запроса
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    // Обработка ответа
    async handleResponse(response) {
        if (response.status === 401) {
            // Токен недействителен, выходим из системы
            this.removeToken();
            window.location.href = '/login';
            throw new Error('Необходима авторизация');
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP Error: ${response.status}`);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }

        return await response.text();
    }

    // GET запрос
    async get(endpoint, params = {}) {
        const url = new URL(`${this.baseURL}${endpoint}`);
        Object.keys(params).forEach(key => {
            if (params[key] !== undefined && params[key] !== null) {
                url.searchParams.append(key, params[key]);
            }
        });

        console.log(`[API] GET ${url.toString()}`);

        const response = await fetch(url.toString(), {
            method: 'GET',
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    // POST запрос
    async post(endpoint, data = null, config = {}) {
        const url = `${this.baseURL}${endpoint}`;
        console.log(`[API] POST ${url}`, data);

        const body = data ? JSON.stringify(data) : null;

        const response = await fetch(url, {
            method: 'POST',
            headers: this.getHeaders(),
            body: body,
            ...config
        });

        return this.handleResponse(response);
    }

    // PUT запрос
    async put(endpoint, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        console.log(`[API] PUT ${url}`, data);

        const body = data ? JSON.stringify(data) : null;

        const response = await fetch(url, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: body,
        });

        return this.handleResponse(response);
    }

    // DELETE запрос
    async delete(endpoint, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        console.log(`[API] DELETE ${url}`);

        const body = data ? JSON.stringify(data) : null;

        const response = await fetch(url, {
            method: 'DELETE',
            headers: this.getHeaders(),
            body: body,
        });

        return this.handleResponse(response);
    }
}

export default new ApiService(); 