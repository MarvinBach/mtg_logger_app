from typing import List, Dict, Any, Optional
from config.config import config
from core.models import Player, Game
from datetime import datetime, timedelta

class PlayerRepository:
    """Repository for player-related database operations"""
    @staticmethod
    def add(name: str) -> Dict[str, Any]:
        try:
            player = Player(name=name)
            player.validate()

            config.logger.info(f"Adding new player: {name}")
            response = config.db.table("players").insert({"name": name.strip()}).execute()

            if not response.data:
                raise Exception("No data returned from database")
            return response.data[0]
        except Exception as e:
            config.logger.error(f"Failed to add player: {str(e)}")
            raise ValueError(f"Failed to add player: {str(e)}")

    @staticmethod
    def delete(player_id: int) -> None:
        try:
            config.logger.info(f"Deleting player with ID: {player_id}")
            response = config.db.table("players").delete().eq("id", player_id).execute()
            if not response.data:
                raise Exception("No data returned from database")
        except Exception as e:
            config.logger.error(f"Failed to delete player: {str(e)}")
            raise ValueError(f"Failed to delete player: {str(e)}")

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        try:
            response = config.db.table("players").select("*").execute()
            return response.data
        except Exception as e:
            config.logger.error(f"Failed to fetch players: {str(e)}")
            return []

    @staticmethod
    def get_by_id(player_id: int) -> Optional[str]:
        try:
            response = (
                config.db.table("players")
                .select("name")
                .eq("id", player_id)
                .limit(1)
                .execute()
            )
            return response.data[0]["name"] if response.data else None
        except Exception as e:
            config.logger.error(f"Failed to fetch player {player_id}: {str(e)}")
            return None


class GameRepository:
    """Repository for game-related database operations"""
    @staticmethod
    def add(game: Game) -> Dict[str, Any]:
        try:
            game.validate()
            config.logger.info(f"Adding new game: {game}")

            response = config.db.table("games").insert(game.to_dict()).execute()
            if not response.data:
                raise Exception("No data returned from database")
            return response.data[0]
        except Exception as e:
            config.logger.error(f"Failed to add game: {str(e)}")
            raise ValueError(f"Failed to add game: {str(e)}")

    @staticmethod
    def update(game_id: int, game: Game) -> Dict[str, Any]:
        """Update an existing game"""
        try:
            game.validate()
            config.logger.info(f"Updating game {game_id}: {game}")

            game_data = game.to_dict()
            response = config.db.table("games").update(game_data).eq("id", game_id).execute()

            if not response.data:
                raise Exception("No data returned from database")
            return response.data[0]
        except Exception as e:
            config.logger.error(f"Failed to update game {game_id}: {str(e)}")
            raise ValueError(f"Failed to update game: {str(e)}")

    @staticmethod
    def delete(game_id: int) -> None:
        try:
            config.logger.info(f"Deleting game with ID: {game_id}")
            response = config.db.table("games").delete().eq("id", game_id).execute()
            if not response.data:
                raise Exception("No data returned from database")
        except Exception as e:
            config.logger.error(f"Failed to delete game {game_id}: {str(e)}")
            raise ValueError(f"Failed to delete game: {str(e)}")

    @staticmethod
    def get_filtered_games(
        start_date=None,
        end_date=None,
        edition_filter="All",
        format_filter="All",
        player_id=None,
        limit=None
    ) -> List[Dict[str, Any]]:
        """Get games with filters applied at database level"""
        try:
            # Build base query with common filters
            def apply_common_filters(query):
                if start_date:
                    query = query.gte("played_at", start_date.isoformat())
                if end_date:
                    # Add one day to include the end date fully
                    next_day = end_date + timedelta(days=1)
                    query = query.lt("played_at", next_day.isoformat())
                if edition_filter != "All":
                    query = query.eq("edition", edition_filter)
                if format_filter != "All":
                    query = query.eq("format", format_filter)
                return query

            # If player filter is active, combine winner and loser games
            if player_id:
                # Get games where player is winner
                winner_query = config.db.table("games").select("*")
                winner_query = apply_common_filters(winner_query)
                winner_games = winner_query.eq("winner_id", player_id).execute().data

                # Get games where player is loser
                loser_query = config.db.table("games").select("*")
                loser_query = apply_common_filters(loser_query)
                loser_games = loser_query.eq("loser_id", player_id).execute().data

                # Combine and sort the results
                all_games = winner_games + loser_games
                all_games.sort(key=lambda x: x["played_at"], reverse=True)
                return all_games[:limit] if limit else all_games

            # If no player filter, use single query with all filters
            query = config.db.table("games").select("*")
            query = apply_common_filters(query)
            query = query.order("played_at", desc=True)
            if limit:
                query = query.limit(limit)

            return query.execute().data
        except Exception as e:
            config.logger.error(f"Failed to fetch filtered games: {str(e)}")
            return []

    @staticmethod
    def get_recent(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            query = config.db.table("games").select("*").order("played_at", desc=True)
            if limit is not None:
                query = query.limit(limit)
            return query.execute().data
        except Exception as e:
            config.logger.error(f"Failed to fetch recent games: {str(e)}")
            return []

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        try:
            return config.db.table("games").select("*").execute().data
        except Exception as e:
            config.logger.error(f"Failed to fetch all games: {str(e)}")
            return []

    @staticmethod
    def get_by_player(player_id: int) -> List[Dict[str, Any]]:
        try:
            return config.db.table("games").select("*").or_(
                f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
            ).execute().data
        except Exception as e:
            config.logger.error(f"Failed to fetch games for player {player_id}: {str(e)}")
            return []

    @staticmethod
    def get_by_id(game_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific game by ID"""
        try:
            response = config.db.table("games").select("*").eq("id", game_id).limit(1).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            config.logger.error(f"Failed to fetch game {game_id}: {str(e)}")
            return None
