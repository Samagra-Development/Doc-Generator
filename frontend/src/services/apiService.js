import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:3000';

export const generateRender = async (templateType, templateInput, data) => {
  try {
    const requestBody = {
      templateContent: templateInput,
      data: data,
      engineType: templateType,
    };

    const response = await axios.post(
      `${API_BASE_URL}/api/generate/render`,
      requestBody,
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createBatch = async (templateType, templateID, payload) => {
  try {
    const requestBody = {
      templateType: templateType,
      templateID: templateID,
      payload: payload,
    };

    const response = await axios.post(
      `${API_BASE_URL}/api/generate/batches`,
      requestBody,
    );

    return response.data;
  } catch (error) {
    throw error;
  }
};

export const fetchBatches = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/generate/batches`);
    if (response.status === 200) {
      return response.data;
    } else {
      console.error('Failed to fetch batches:', response.status);
      return [];
    }
  } catch (error) {
    console.error('Error fetching batches:', error);
    return [];
  }
};

export const fetchTemplates = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/template`);
    if (response.status === 200) {
      return response.data;
    } else {
      console.error('Failed to fetch templates:', response.status);
      return [];
    }
  } catch (error) {
    console.error('Error fetching templates:', error);
    return [];
  }
};
