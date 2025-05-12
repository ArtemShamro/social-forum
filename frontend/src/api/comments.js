import api from "../api/axiosInstance";

export async function ListComments({ postId, page, perPage }) {
  try {
    const response = await api.get(
      `/posts/list_comments?post_id=${postId}&page=${page}&per_page=${perPage}`
    );
    console.log("api function ListComments:", postId, response.data);

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function CreateComment({ postId, comment }) {
  console.log("api function CreateComment:", postId, comment);
  const data = { post_id: Number(postId), comment: comment };
  try {
    const response = await api.post("/posts/create_comment", data);
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
