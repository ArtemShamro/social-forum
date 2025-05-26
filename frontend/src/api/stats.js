import api from "./axiosInstance";

export async function getTopUsers({ metric }) {
  try {
    const response = await api.get(
      `/stats/get_top_users?target_type=${metric}`
    );
    console.log("api function getTopUsers:", metric, response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching rankings:", error);
    return null;
  }
}

export async function getTopPosts({ metric }) {
  console.log("getTopPosts", metric);
  try {
    const response = await api.get(
      `/stats/get_top_posts?target_type=${metric}`
    );
    console.log("api function getTopPosts:", metric, response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching rankings:", error);
    return null;
  }
}

export async function GetPostStats(postId, targetType) {
  // Adjust the endpoint as needed
  const res = await api.get(`/stats/get_post_stats?post_id=${postId}`);
  console.log("api function GetPostStat:", postId, res.data);
  return res.data;
}