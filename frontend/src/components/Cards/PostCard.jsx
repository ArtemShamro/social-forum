import React from "react";
import styles from "./PostCard.module.css";
import { useNavigate } from "react-router-dom";

export default function PostCard({ post }) {
  const router = useNavigate();

  return (
    <div
      className={styles.card}
      onClick={() => router(`/post/${post.postId}`, { replace: true })}
    >
      <h2 className={styles.title}>
        {post.postId} {post.title}
      </h2>
      <p className={styles.description}>{post.description}</p>
      <div className={styles.footer}>
        <span className={styles.date}>
          {new Date(post.createdAt).toLocaleDateString()}
        </span>
        {post.private && <span className={styles.badge}>Private</span>}
      </div>
    </div>
  );
}
