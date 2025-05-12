import React from "react";
import { ListComments } from "../api/comments";
import CommentCard from "./Cards/CommentCard";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import CommentCardCard from "./Cards/CommentCard";

export default function CommentSection({ postId }) {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    const fetchComments = async () => {
      const data = await ListComments({
        postId: Number(postId),
        page: 1,
        perPage: 10,
      });
      setComments(data || []);
    };
    fetchComments();
  }, []);

  if (comments.length === 0) return <p>Посты не найдены.</p>;

  return (
    <section className="comment-section">
      {comments.map((comment) => (
        <CommentCardCard key={comment.commentId} comment={comment} />
      ))}
    </section>
  );
}
