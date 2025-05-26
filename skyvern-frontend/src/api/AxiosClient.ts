import { apiBaseUrl, artifactApiBaseUrl, envCredential } from "@/util/env";
import axios from "axios";

const apiV1BaseUrl = apiBaseUrl;
const apiV2BaseUrl = apiBaseUrl.replace("v1", "v2");

// Create clients without API key initially
const client = axios.create({
  baseURL: apiV1BaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

const v2Client = axios.create({
  baseURL: apiV2BaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

// Initialize API key
let apiKeyInitialized = false;

async function initializeApiKey() {
  if (apiKeyInitialized) return;
  
  try {
    // Try to fetch API key from the backend config endpoint
    const response = await fetch('/api/config');
    if (response.ok) {
      const config = await response.json();
      if (config.apiKey) {
        setApiKeyHeader(config.apiKey);
        console.log("API key loaded from backend config");
        apiKeyInitialized = true;
        return;
      }
    }
  } catch (error) {
    console.warn("Failed to fetch API key from backend config:", error);
  }
  
  // Fallback to environment variable
  if (envCredential) {
    setApiKeyHeader(envCredential);
    console.log("API key loaded from environment variable");
    apiKeyInitialized = true;
  } else {
    console.warn("No API key available");
  }
}

const artifactApiClient = axios.create({
  baseURL: artifactApiBaseUrl,
});

export function setAuthorizationHeader(token: string) {
  client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  v2Client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function removeAuthorizationHeader() {
  if (client.defaults.headers.common["Authorization"]) {
    delete client.defaults.headers.common["Authorization"];
    delete v2Client.defaults.headers.common["Authorization"];
  }
}

export function setApiKeyHeader(apiKey: string) {
  client.defaults.headers.common["X-API-Key"] = apiKey;
  v2Client.defaults.headers.common["X-API-Key"] = apiKey;
}

export function removeApiKeyHeader() {
  if (client.defaults.headers.common["X-API-Key"]) {
    delete client.defaults.headers.common["X-API-Key"];
  }
  if (v2Client.defaults.headers.common["X-API-Key"]) {
    delete v2Client.defaults.headers.common["X-API-Key"];
  }
}

async function getClient(
  credentialGetter: CredentialGetter | null,
  version: string = "v1",
) {
  // Ensure API key is initialized
  await initializeApiKey();
  
  if (credentialGetter) {
    removeApiKeyHeader();
    const credential = await credentialGetter();
    if (!credential) {
      console.warn("No credential found");
      return version === "v1" ? client : v2Client;
    }
    setAuthorizationHeader(credential);
  }
  return version === "v1" ? client : v2Client;
}

export type CredentialGetter = () => Promise<string | null>;

export { getClient, artifactApiClient, initializeApiKey };
