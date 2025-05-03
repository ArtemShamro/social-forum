import React from "react";
import { useState, useEffect } from "react";
import PostCard from "./Cards/PostCard";
import { ListPosts } from "../api/posts";

export default function PostsSection() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const data = await ListPosts({ page: 1, perPage: 10 });
      setPosts(data || []);
    };
    fetchPosts();
  }, []);

  if (posts.length === 0) return <p>Посты не найдены.</p>;

  return (
    <section className="posts-section">
      {posts.map((post) => (
        <PostCard key={post.postId} post={post} />
      ))}
    </section>
  );
}
