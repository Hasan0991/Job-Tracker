import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "https://ravishing-vibrancy-production.up.railway.app", 
});

export default API;
