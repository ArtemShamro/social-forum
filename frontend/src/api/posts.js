import api from "../api/axiosInstance";

export async function ListPosts({ page, perPage }) {
  try {
    const response = await api.get(
      `/posts/list_posts?page=${page}&per_page=${perPage}`
    );
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function NewPost({ title, description, is_private }) {
  const data = { title: title, description: description, private: is_private };
  try {
    const response = await api.post("/posts/create_post", data);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function GetPostById(id) {
  console.log(id);
  const data = { post_id: id };
  try {
    const response = await api.post(`/posts/get_post`, data);
    
    console.log("RESPONSE:", response.data);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}
