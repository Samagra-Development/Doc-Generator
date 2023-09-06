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
