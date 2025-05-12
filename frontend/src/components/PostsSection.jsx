import React from "react";
import { useState, useEffect } from "react";
import PostCard from "./Cards/PostCard";
import { ListPosts } from "../api/posts";
import { Pagination } from "antd";

export default function PostsSection() {
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalPosts, setTotalPosts] = useState(0);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const data = await ListPosts({ page: currentPage, perPage: pageSize });
      setPosts(data || []);
    };
    fetchPosts();
  }, [currentPage, pageSize]);

  if (posts.length === 0) return <p>Посты не найдены.</p>;

  return (
    <section className="posts-section" style={{ padding: "0px" }}>
      <div
        style={{
          background: "#f9f9f9",
          borderRadius: "12px",
          padding: "20px 0",
          margin: "24px 0",
          boxShadow: "0 2px 12px rgba(0,0,0,0.07)",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Pagination
          current={currentPage}
          pageSize={pageSize}
          total={totalPosts}
          showQuickJumper
          showSizeChanger
          pageSizeOptions={["5", "10", "20", "50"]}
          onChange={(page, size) => {
            setCurrentPage(page);
            setPageSize(size);
          }}
          itemRender={(page, type, originalElement) => {
            if (type === "prev") {
              return (
                <button
                  style={{
                    border: "none",
                    background: "none",
                    color: "#1890ff",
                  }}
                >
                  « Prev
                </button>
              );
            }
            if (type === "next") {
              return (
                <button
                  style={{
                    border: "none",
                    background: "none",
                    color: "#1890ff",
                  }}
                >
                  Next »
                </button>
              );
            }
            return originalElement;
          }}
        />
      </div>
      {posts.map((post) => (
        <PostCard key={post.postId} post={post} />
      ))}
    </section>
  );
}
