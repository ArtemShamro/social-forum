import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { GetPostById } from "../api/posts";
import classes from "./PostIdPage.module.css";
import CommentSection from "../components/CommentSection";
import { AuthContext } from "../Context";
import NewCommentForm from "../components/Forms/NewCommnetForm/NewCommentForm";

export default function Posts() {
  const params = useParams();
  const [post, setPost] = useState([]);
  const [userId, userName] = useContext(AuthContext);

  useEffect(() => {
    const fetchPost = async () => {
      const data = await GetPostById(params.id);
      setPost(data || []);
    };
    fetchPost();
  }, []);

  console.log(params);
  return (
    <section>
      <div className={classes.container}>
        <h1 className={classes.title}>{post.title}</h1>
        <p className={classes.meta}>
          Автор: {post.ownerId} | Опубликовано:{" "}
          {new Date(post.createdAt).toLocaleDateString()}
        </p>
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
