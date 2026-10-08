// API client for LiveCodeAI backend services
const PORT = 8000;
export const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? `http://${window.location.hostname}:${PORT}`
  : window.location.origin;

function getHeaders(extraHeaders = {}) {
  const token = localStorage.getItem("access_token");
  const headers = { ...extraHeaders };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

/**
 * Register a new user profile.
 */
export async function registerApi(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Registration failed.');
  }
  return await response.json();
}

/**
 * Log in a user.
 */
export async function loginApi(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Login failed.');
  }
  const data = await response.json();
  // Save to local storage
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("user_email", data.user.email);
  localStorage.setItem("user_role", data.user.role);
  return data;
}

/**
 * Logs out user by clearing storage.
 */
export function logoutApi() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_email");
  localStorage.removeItem("user_role");
}

/**
 * Creates a new sandboxed session in the backend.
 * @returns {Promise<string>} session_id
 */
export async function createSessionApi() {
  const response = await fetch(`${API_BASE_URL}/session/create`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
  });
  if (!response.ok) {
    throw new Error('Failed to create backend session workspace.');
  }
  const data = await response.json();
  return data.session_id;
}

/**
 * Destroys a sandboxed session workspace in the backend.
 * @param {string} sessionId 
 */
export async function destroySessionApi(sessionId) {
  const response = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!response.ok) {
    throw new Error(`Failed to destroy session: ${sessionId}`);
  }
}

/**
 * Fetches the hierarchical file list tree.
 * @param {string} sessionId 
 * @returns {Promise<Array>} fileTree nodes list
 */
export async function fetchFileTree(sessionId) {
  const response = await fetch(`${API_BASE_URL}/files/${sessionId}`, {
    headers: getHeaders()
  });
  if (!response.ok) {
    throw new Error('Failed to retrieve file explorer directory tree.');
  }
  const data = await response.json();
  return data.files || [];
}

/**
 * Reads a single file's contents.
 * @param {string} sessionId 
 * @param {string} filePath 
 * @returns {Promise<object>} { path, content, language }
 */
export async function readFileContent(sessionId, filePath) {
  const encodedPath = filePath.split('/').map(encodeURIComponent).join('/');
  const response = await fetch(`${API_BASE_URL}/files/${sessionId}/${encodedPath}`, {
    headers: getHeaders()
  });
  if (!response.ok) {
    throw new Error(`Failed to read file: ${filePath}`);
  }
  return await response.json();
}

/**
 * Saves a file's content to the backend sandbox on disk.
 * @param {string} sessionId 
 * @param {string} filePath 
 * @param {string} content 
 */
export async function saveFileContent(sessionId, filePath, content) {
  const encodedPath = filePath.split('/').map(encodeURIComponent).join('/');
  const response = await fetch(`${API_BASE_URL}/files/${sessionId}/${encodedPath}`, {
    method: 'PUT',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ content }),
  });
  if (!response.ok) {
    throw new Error(`Failed to save file: ${filePath}`);
  }
}

/**
 * Creates a file or directory node inside the session workspace.
 * @param {string} sessionId 
 * @param {string} parentPath 
 * @param {string} name 
 * @param {string} type 'file' | 'directory'
 * @param {string} content 
 */
export async function createFileNode(sessionId, parentPath, name, type, content = "") {
  const path = parentPath ? `${parentPath}/${name}` : name;
  const response = await fetch(`${API_BASE_URL}/files/${sessionId}`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ path, type, content }),
  });
  if (!response.ok) {
    throw new Error(`Failed to create workspace ${type} at ${path}`);
  }
}

/**
 * Deletes a file or directory recursively.
 * @param {string} sessionId 
 * @param {string} filePath 
 */
export async function deleteFileNode(sessionId, filePath) {
  const encodedPath = filePath.split('/').map(encodeURIComponent).join('/');
  const response = await fetch(`${API_BASE_URL}/files/${sessionId}/${encodedPath}`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!response.ok) {
    throw new Error(`Failed to delete path: ${filePath}`);
  }
}

/**
 * Runs code inside the session workspace.
 * @param {string} sessionId
 * @param {string} filePath
 * @returns {Promise<object>} { stdout, stderr, exit_code }
 */
export async function runCodeApi(sessionId, filePath) {
  const response = await fetch(`${API_BASE_URL}/run/${sessionId}`, {
    method: 'POST',
    headers: getHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ path: filePath }),
  });
  if (!response.ok) {
    throw new Error(`Failed to execute code: ${filePath}`);
  }
  return await response.json();
}

/**
 * Fetches monitor dashboard analytics.
 */
export async function fetchMetricsApi() {
  const response = await fetch(`${API_BASE_URL}/admin/metrics`, {
    headers: getHeaders()
  });
  if (!response.ok) {
    throw new Error('Failed to fetch admin metrics.');
  }
  return await response.json();
}

/**
 * Triggers engagement heartbeat ping.
 */
export async function pingEngagementApi(sessionId) {
  await fetch(`${API_BASE_URL}/engagement/ping`, {
    method: 'POST',
    headers: getHeaders({ 
      'Content-Type': 'application/json',
      'X-Session-ID': sessionId 
    })
  });
}

/**
 * Returns the correct WebSocket endpoint based on hostname
 * @param {string} sessionId
 * @returns {string} wsUrl
 */
export function getWebSocketUrl(sessionId) {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const token = localStorage.getItem("access_token") || "mock_token";
  const suffix = `?token=${encodeURIComponent(token)}`;
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return `${wsProtocol}//${window.location.hostname}:${PORT}/ws/${sessionId}${suffix}`;
  }
  return `${wsProtocol}//${window.location.host}/ws/${sessionId}${suffix}`;
}
