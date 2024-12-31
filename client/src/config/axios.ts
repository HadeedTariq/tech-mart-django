import axios from "axios";

const accountApi = axios.create({
  baseURL: "http://localhost:3000/auth",
  withCredentials: true,
});
const productApi = axios.create({
  baseURL: "http://localhost:3000/product",
  withCredentials: true,
});
const adminApi = axios.create({
  baseURL: "http://localhost:3000/admin",
  withCredentials: true,
});
const sellerApi = axios.create({
  baseURL: "http://localhost:3000/seller",
  withCredentials: true,
});
const chatApi = axios.create({
  baseURL: "http://localhost:3000/chats",
  withCredentials: true,
});

export { accountApi, productApi, adminApi, sellerApi, chatApi };
