import React from "react";
import styles from "./CommentCard.module.css";
import { useNavigate } from "react-router-dom";

export default function CommentCard({ comment }) {
  const router = useNavigate();

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>
        {comment.commentId} {comment.userId}
      </h2>
      <p className={styles.description}>{comment.comment}</p>
      <div className={styles.footer}>
        <span className={styles.date}>
          {new Date(comment.createdAt).toLocaleDateString()}
        </span>
      </div>
    </div>
  );
}

// {commentId: 1, commentId: 1, userId: '34', comment: 'Comment to comment 1', createdAt: '2025-04-15T09:07:01.421684'}
