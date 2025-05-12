import React, { useState, useEffect } from "react";
import { Tabs, Card, List, Avatar, Typography } from "antd";
import { LikeOutlined, EyeOutlined, CommentOutlined } from "@ant-design/icons";
import { getTopUsers, getTopPosts } from "../../api/stats";
import styles from "./RankingsSection.module.css";

const { Title } = Typography;

const RankingsSection = () => {
  const [popularPosts, setPopularPosts] = useState([]);
  const [topUsers, setTopUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingPosts, setLoadingPosts] = useState(false);
  const [loadingUsers, setLoadingUsers] = useState(false);

  const fetchRankings = async (target, metric) => {
    setLoading(true);
    try {
      let data;
      if (target === "post") {
        data = await getTopPosts({ metric });
      } else {
        data = await getTopUsers({ metric });
      }
      return data;
    } catch (error) {
      console.error("Error fetching rankings:", error);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const handlePostTabChange = async (key) => {
    setLoadingPosts(true);
    const data = await fetchRankings("post", key);
    setLoadingPosts(false);
    if (Array.isArray(data)) {
      data.sort((a, b) => (b.value ?? 0) - (a.value ?? 0));
      setPopularPosts(data);
    } else {
      setPopularPosts([]);
    }
  };

  const handleUserTabChange = async (key) => {
    setLoadingUsers(true);
    const data = await fetchRankings("user", key);
    setLoadingUsers(false);
    if (Array.isArray(data)) {
      data.sort((a, b) => (b.value ?? 0) - (a.value ?? 0));
      setTopUsers(data);
    } else {
      setTopUsers([]);
    }
  };

  const postItems = [
    {
      key: "like",
      label: "Likes",
      icon: <LikeOutlined />,
    },
    {
      key: "view",
      label: "Views",
      icon: <EyeOutlined />,
    },
    {
      key: "comment",
      label: "Comments",
      icon: <CommentOutlined />,
    },
  ];

  const userItems = [
    {
      key: "post",
      label: "Posts",
      icon: <LikeOutlined />,
    },
    {
      key: "like",
      label: "Likes",
      icon: <LikeOutlined />,
    },
    {
      key: "comment",
      label: "Comments",
      icon: <CommentOutlined />,
    },
  ];

  useEffect(() => {
    handlePostTabChange("like");
    handleUserTabChange("post");
  }, []);

  return (
    <div className={styles.rankingsContainer}>
      <Card className={styles.rankingCard}>
        <Title level={4}>Popular Posts</Title>
        <Tabs
          items={postItems}
          onChange={handlePostTabChange}
          className={styles.tabs}
        />
        <List
          loading={loadingPosts}
          dataSource={popularPosts}
          renderItem={(post) => (
            <List.Item>
              <List.Item.Meta
                avatar={
                  <div
                    style={{
                      width: 40,
                      height: 40,
                      borderRadius: "50%",
                      background: "#faad14",
                      color: "#fff",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: "bold",
                      fontSize: 18,
                    }}
                  >
                    {post.value}
                  </div>
                }
                title={<a href={`/post/${post.id}`}>{post.title}</a>}
                // Optionally, show the value label
                description={`Value: ${post.value}`}
              />
            </List.Item>
          )}
        />
      </Card>

      <Card className={styles.rankingCard}>
        <Title level={4}>Top Users</Title>
        <Tabs
          items={userItems}
          onChange={handleUserTabChange}
          className={styles.tabs}
        />
        <List
          loading={loadingUsers}
          dataSource={topUsers}
          renderItem={(user) => (
            <List.Item>
              <List.Item.Meta
                avatar={
                  <div
                    style={{
                      width: 40,
                      height: 40,
                      borderRadius: "50%",
                      background: "#1890ff",
                      color: "#fff",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: "bold",
                      fontSize: 18,
                    }}
                  >
                    {user.value}
                  </div>
                }
                title={
                  <a href={`/profile/${user.id}`}>
                    {user.name} {user.surname}
                  </a>
                }
                description={user.surname}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default RankingsSection;
