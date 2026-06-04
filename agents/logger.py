"""
logger.py — Sistema de logging centralizado para eventos dos agentes.

Fornece um EventLogger thread-safe que armazena eventos em filas por request_id,
permitindo streaming via SSE para o frontend e também exibição no terminal.
"""

import sys
import threading
from datetime import datetime
from queue import Queue
from typing import Optional


class LogEvent:
    """Representa um evento de log."""

    def __init__(self, agent: str, level: str, message: str):
        self.timestamp = datetime.now().isoformat()
        self.agent = agent
        self.level = level  # info, success, warning, error
        self.message = message

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "agent": self.agent,
            "level": self.level,
            "message": self.message,
        }

    def __repr__(self):
        return f"[{self.timestamp}] [{self.agent.upper()}] [{self.level.upper()}] {self.message}"


class EventLogger:
    """Logger thread-safe que mantém filas de eventos por request_id."""

    def __init__(self):
        self._queues: dict[str, Queue] = {}
        self._lock = threading.Lock()

    def create_queue(self, request_id: str) -> Queue:
        """Cria uma nova fila para um request_id."""
        with self._lock:
            self._queues[request_id] = Queue()
            return self._queues[request_id]

    def remove_queue(self, request_id: str):
        """Remove a fila de um request_id após o término."""
        with self._lock:
            self._queues.pop(request_id, None)

    def get_queue(self, request_id: str) -> Optional[Queue]:
        with self._lock:
            return self._queues.get(request_id)

    def log(self, request_id: str, agent: str, level: str, message: str):
        """Registra um evento e o envia para a fila do request_id."""
        event = LogEvent(agent, level, message)

        # Print no terminal
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{agent.upper()}] [{level.upper()}] {message}",
            flush=True,
        )

        # Envia para a fila SSE
        q = self.get_queue(request_id)
        if q:
            q.put(event)


# Instância global
event_logger = EventLogger()


# Funções auxiliares para facilitar o uso
def log_info(request_id: str, agent: str, message: str):
    event_logger.log(request_id, agent, "info", message)


def log_success(request_id: str, agent: str, message: str):
    event_logger.log(request_id, agent, "success", message)


def log_warning(request_id: str, agent: str, message: str):
    event_logger.log(request_id, agent, "warning", message)


def log_error(request_id: str, agent: str, message: str):
    event_logger.log(request_id, agent, "error", message)
