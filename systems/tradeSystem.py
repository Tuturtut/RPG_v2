from components.base import Delete


class TradeSystem:
    def update(self, entities, world_state):
        # On cherche les "entités-tickets" de transaction
        for t in entities:
            ticket = entities[t]
            request = ticket.get_comp("TradeRequest")
            
            if not request or request.status != "PENDING":
                continue


            # On récupère les inventaires des deux parties
            inv_sender = request.sender.get_comp("Inventory")

            inv_receiver = request.receiver.get_comp("Inventory")

            if inv_sender and inv_receiver:
                if request.item in inv_sender.items:
                    # EXECUTION DU TRANSFERT
                    inv_sender.items.remove(request.item)
                    inv_receiver.items.append(request.item)
                    
                    request.status = "COMPLETED"
                else:
                    request.status = "FAILED"
                
            
            # Une fois traitée, on pourra supprimer cette entité au tour suivant
            ticket.add_comp(Delete()) # Un tag pour dire "À supprimer"