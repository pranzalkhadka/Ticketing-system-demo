from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uvicorn
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: str = "None"
    created_at: datetime

class TicketCreate(BaseModel):
    title: str
    description: str

TICKETS_FILE = "/data/tickets.json"

def load_tickets():
    if not os.path.exists(TICKETS_FILE):
        return {"tickets": [], "ticket_id_counter": 1}
    with open(TICKETS_FILE, "r") as f:
        data = json.load(f)
        for ticket in data["tickets"]:
            ticket["created_at"] = datetime.fromisoformat(ticket["created_at"])
        return data

def save_tickets(tickets, ticket_id_counter):
    os.makedirs(os.path.dirname(TICKETS_FILE), exist_ok=True)
    with open(TICKETS_FILE, "w") as f:
        serializable_tickets = [
            {**ticket.dict(), "created_at": ticket.created_at.isoformat()}
            for ticket in tickets
        ]
        json.dump({"tickets": serializable_tickets, "ticket_id_counter": ticket_id_counter}, f, indent=2)

data = load_tickets()
tickets = [Ticket(**ticket) for ticket in data["tickets"]]
ticket_id_counter = data["ticket_id_counter"]

@app.post("/tickets", response_model=Ticket)
async def create_ticket(ticket: TicketCreate):
    global ticket_id_counter
    new_ticket = Ticket(
        id=ticket_id_counter,
        title=ticket.title,
        description=ticket.description,
        status="None",
        created_at=datetime.utcnow()
    )
    tickets.append(new_ticket)
    ticket_id_counter += 1
    save_tickets(tickets, ticket_id_counter)
    return new_ticket

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.put("/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: int, status: str):
    for ticket in tickets:
        if ticket.id == ticket_id:
            ticket.status = status
            save_tickets(tickets, ticket_id_counter)
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    for i, ticket in enumerate(tickets):
        if ticket.id == ticket_id:
            tickets.pop(i)
            save_tickets(tickets, ticket_id_counter)
            return {"message": "Ticket deleted"}
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.get("/tickets", response_model=List[Ticket])
async def list_tickets():
    return tickets

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)