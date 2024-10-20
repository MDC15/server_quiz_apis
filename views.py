import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
from controllers import PlayerController
import logging


def show_ranking():
    st.header("Player Rankings")
    player_controller = PlayerController()

    # Lấy bảng xếp hạng
    rankings = player_controller.get_ranking(limit=500)

    if not rankings:
        st.info("No rankings available yet.")
        return

    df = pd.DataFrame(rankings)

    # Thêm STT bắt đầu từ 1 và ẩn cột 'items'
    df.insert(0, "STT", range(1, len(df) + 1))
    if "items" in df.columns:
        df = df.drop("items", axis=1)

    # Kiểm tra xem có dữ liệu và cột score không
    if not df.empty and "name" in df.columns:
        # Add styling to the dataframe
        styled_df = df.style.highlight_max(
            subset=["name"], color="black", axis=0
        ).highlight_min(subset=["name"], color="black", axis=0)

        # Hiển thị bảng dữ liệu đã được định dạng
        st.dataframe(styled_df, use_container_width=True)
    else:
        # Hiển thị DataFrame gốc nếu không có cột score
        st.dataframe(df)

    # Thêm thông tin chi tiết
    if not df.empty:
        st.markdown("### Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Players", len(df))

        if "score" in df.columns:
            with col2:
                st.metric("Highest Score", df["score"].max())
            with col3:
                st.metric("Average Score", round(df["score"].mean(), 2))

    if st.button("Refresh Rankings"):
        st.session_state.refresh_rankings = True


def show_logs():
    st.header("Application Logs")

    # Add log filtering options
    log_filter = st.selectbox(
        "Filter logs by level:", ["All", "INFO", "WARNING", "ERROR"]
    )

    try:
        with open("quiz_app.log", "r") as f:
            logs = f.readlines()

        filtered_logs = logs
        if log_filter != "All":
            filtered_logs = [log for log in logs if log_filter in log]

        if filtered_logs:
            st.text_area("Logs", "".join(filtered_logs), height=500)
        else:
            st.info("No logs found for the selected filter.")

    except FileNotFoundError:
        st.warning(
            "Log file not found. It will be created when the application generates logs."
        )

    if st.button("Refresh Logs"):
        st.session_state.refresh_logs = True


def show_management():
    st.header("Player Management")
    player_controller = PlayerController()

    # Display current statistics
    try:
        conn = player_controller.db.get_connection()
        total_players = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
        st.metric("Total Players in Database", total_players)
    except Exception as e:
        st.error(f"Error fetching statistics: {str(e)}")
        logging.error(f"Error fetching statistics: {str(e)}")
    finally:
        conn.close()

    # Add confirmation dialog for dangerous operations
    st.warning("⚠️ Danger Zone")
    with st.expander("Delete All Records"):
        st.write(
            "This action will permanently delete all player records from the database."
        )

        confirm_text = st.text_input("Type 'DELETE' to confirm", key="delete_confirm")

        if st.button("Delete All Records", type="primary"):
            if confirm_text == "DELETE1501":
                try:
                    conn = player_controller.db.get_connection()
                    conn.execute("DELETE FROM players")
                    conn.commit()
                    st.success("All records deleted successfully")
                    logging.info("All player records deleted by admin")
                    # Thay thế st.experimental_rerun()
                    st.session_state.records_deleted = True
                except Exception as e:
                    st.error(f"Error deleting records: {str(e)}")
                    logging.error(f"Error deleting records: {str(e)}")
                finally:
                    conn.close()
            else:
                st.error("Please type 'DELETE' to confirm the operation")


# Thêm hàm utility để kiểm tra kết nối database
def check_database_connection():
    try:
        player_controller = PlayerController()
        conn = player_controller.db.get_connection()
        conn.execute("SELECT 1")
        return True
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        return False
    finally:
        if "conn" in locals() and conn:
            conn.close()


# Trong hàm main của bạn
def main():
    if "refresh_rankings" in st.session_state and st.session_state.refresh_rankings:
        # Reset lại trạng thái
        st.session_state.refresh_rankings = False
        show_ranking()

    if "refresh_logs" in st.session_state and st.session_state.refresh_logs:
        # Reset lại trạng thái
        st.session_state.refresh_logs = False
        show_logs()

    if "records_deleted" in st.session_state and st.session_state.records_deleted:
        # Reset lại trạng thái
        st.session_state.records_deleted = False
        show_management()
    else:
        show_management()


if __name__ == "__main__":
    main()
