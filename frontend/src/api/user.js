import api from "../api/axiosInstance";

export async function checkAuth() {
  try {
    const response = await api.get("/utils/get_user"); // автоматически добавится baseURL и заголовки

    return response.data;
  } catch (error) {
    console.error("Пользователь не авторизован", error);
    return null;
  }
}

export async function Login({ username, password }) {
  const data = { login: username, password: password };
  try {
    const response = await api.post("/auth/login", data);

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function Logout() {
  try {
    const response = await api.post("/auth/logout");

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function Register({ username, password, email }) {
  const data = { login: username, password: password, mail: email };
  try {
    const response = await api.post("/auth/register", data);

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function GetMe() {
  try {
    const response = await api.get("/auth/me");
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function UpdateUser({ ...props }) {
  try {
    const response = await api.post("/auth/update", props);

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}
