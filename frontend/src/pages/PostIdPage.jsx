import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { GetPostById, LikePost } from "../api/posts";
import classes from "./PostIdPage.module.css";
import CommentSection from "../components/CommentSection";
import { AuthContext } from "../Context";
import NewCommentForm from "../components/Forms/NewCommnetForm/NewCommentForm";
import { GetPostStats } from "../api/stats";

export default function Posts() {
  const params = useParams();
  const [post, setPost] = useState([]);
  const [userId, userName] = useContext(AuthContext);
  const [stats, setStats] = useState({ views: 0, comments: 0, likes: 0 });

  useEffect(() => {
    const fetchPost = async () => {
      const data = await GetPostById(params.id);
      setPost(data || []);
      // Fetch stats
      const statsData = await GetPostStats(params.id);
      console.log("Stats from API:", statsData);
      setStats(statsData || { views: 0, comments: 0, likes: 0 });
    };
    fetchPost();
  }, [params.id]);

  console.log("Stats in render:", stats);
  console.log(params);
  return (
    <section>
      <div className={classes.container}>
        <h1 className={classes.title}>{post.title}</h1>
        <p className={classes.meta}>
          Автор: {post.ownerId} | Опубликовано:{" "}
          {new Date(post.createdAt).toLocaleDateString()}
        </p>

        <div className={classes.statsRow}>
          <span>👁 {stats.views}</span>
          <span>💬 {stats.comments}</span>
          <span>
            ❤️ {stats.likes}
            {userId && (
              <button
                className={classes.likeButton}
                onClick={async () => {
                  await LikePost(params.id); // Implement this API call
                  // Optionally, refetch likes
                  const updatedStats = await GetPostStats(params.id);
                  setStats(updatedStats || stats);
                }}
              >
                Like
              </button>
            )}
          </span>
        </div>
        <div className={classes.description}>{post.description}</div>
        {post.private && (
          <div className={classes.privateBadge}>Приватный пост</div>
        )}
      </div>
      {userId && <NewCommentForm postId={params.id} />}
      <div className={classes.containerComments}>
        <CommentSection postId={params.id} />
      </div>
    </section>
  );
}
