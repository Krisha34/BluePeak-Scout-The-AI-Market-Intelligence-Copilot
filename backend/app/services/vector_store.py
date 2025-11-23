"""
Vector store service for RAG using ChromaDB
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import app_logger
from sentence_transformers import SentenceTransformer
import uuid


class VectorStore:
    """Vector store for embeddings and semantic search"""

    def __init__(self):
        """Initialize ChromaDB client and embedding model"""
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.CHROMA_PERSIST_DIR
        ))

        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create collections
        self.competitors_collection = self._get_or_create_collection("competitors")
        self.trends_collection = self._get_or_create_collection("trends")
        self.findings_collection = self._get_or_create_collection("findings")
        self.reports_collection = self._get_or_create_collection("reports")

        app_logger.info("Vector store initialized")

    def _get_or_create_collection(self, name: str):
        """Get or create a collection"""
        try:
            return self.client.get_or_create_collection(name)
        except Exception as e:
            app_logger.error(f"Error creating collection {name}: {e}")
            return None

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            app_logger.error(f"Error generating embedding: {e}")
            return []

    async def add_competitor(self, competitor: Dict[str, Any]):
        """Add competitor to vector store"""
        try:
            doc_id = competitor.get("id", str(uuid.uuid4()))
            text = f"{competitor.get('name', '')} {competitor.get('description', '')} {competitor.get('industry', '')}"

            self.competitors_collection.add(
                documents=[text],
                metadatas=[competitor],
                ids=[doc_id]
            )

            app_logger.info(f"Added competitor to vector store: {doc_id}")
        except Exception as e:
            app_logger.error(f"Error adding competitor to vector store: {e}")

    async def add_trend(self, trend: Dict[str, Any]):
        """Add trend to vector store"""
        try:
            doc_id = trend.get("id", str(uuid.uuid4()))
            text = f"{trend.get('title', '')} {trend.get('description', '')} {' '.join(trend.get('keywords', []))}"

            self.trends_collection.add(
                documents=[text],
                metadatas=[trend],
                ids=[doc_id]
            )

            app_logger.info(f"Added trend to vector store: {doc_id}")
        except Exception as e:
            app_logger.error(f"Error adding trend to vector store: {e}")

    async def add_finding(self, finding: Dict[str, Any]):
        """Add research finding to vector store"""
        try:
            doc_id = finding.get("id", str(uuid.uuid4()))
            text = f"{finding.get('title', '')} {finding.get('content', '')}"

            self.findings_collection.add(
                documents=[text],
                metadatas=[finding],
                ids=[doc_id]
            )

            app_logger.info(f"Added finding to vector store: {doc_id}")
        except Exception as e:
            app_logger.error(f"Error adding finding to vector store: {e}")

    async def add_report(self, report: Dict[str, Any]):
        """Add report to vector store"""
        try:
            doc_id = report.get("id", str(uuid.uuid4()))
            text = f"{report.get('title', '')} {report.get('summary', '')} {report.get('content', '')[:1000]}"

            self.reports_collection.add(
                documents=[text],
                metadatas=[report],
                ids=[doc_id]
            )

            app_logger.info(f"Added report to vector store: {doc_id}")
        except Exception as e:
            app_logger.error(f"Error adding report to vector store: {e}")

    async def search(
        self,
        query: str,
        collection_name: str = "all",
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Search across collections"""
        try:
            results = []

            collections = {
                "competitors": self.competitors_collection,
                "trends": self.trends_collection,
                "findings": self.findings_collection,
                "reports": self.reports_collection
            }

            search_collections = (
                collections.values() if collection_name == "all"
                else [collections.get(collection_name)]
            )

            for collection in search_collections:
                if collection:
                    search_results = collection.query(
                        query_texts=[query],
                        n_results=n_results
                    )

                    # Format results
                    if search_results and search_results.get("metadatas"):
                        for i, metadata in enumerate(search_results["metadatas"][0]):
                            results.append({
                                "metadata": metadata,
                                "distance": search_results["distances"][0][i] if "distances" in search_results else 0,
                                "document": search_results["documents"][0][i] if "documents" in search_results else ""
                            })

            # Sort by distance (relevance)
            results.sort(key=lambda x: x["distance"])

            return results[:n_results]
        except Exception as e:
            app_logger.error(f"Error searching vector store: {e}")
            return []

    async def search_similar(
        self,
        text: str,
        collection_name: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Find similar documents"""
        return await self.search(text, collection_name, n_results)


# Global instance
vector_store = VectorStore()
