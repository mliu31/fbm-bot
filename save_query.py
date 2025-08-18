import json
import os
from typing import List, Dict
from datetime import datetime

class QueryManager:
    def __init__(self, filename: str = "saved_queries.json"):
        self.filename = filename
        self.queries = self.load_queries()
    
    def load_queries(self) -> List[Dict]:
        """Load saved queries from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading queries: {e}")
        return []
    
    def save_queries(self):
        """Save queries to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.queries, f, indent=2)
            print(f"Queries saved to {self.filename}")
        except Exception as e:
            print(f"Error saving queries: {e}")
    
    def add_query(self, keyword: str, location: str = None, min_price: int = None, 
                  max_price: int = None, active: bool = True):
        """Add a new search query"""
        query = {
            'id': len(self.queries) + 1,
            'keyword': keyword,
            'location': location,
            'min_price': min_price,
            'max_price': max_price,
            'active': active,
            'created_at': datetime.now().isoformat()
        }
        
        self.queries.append(query)
        self.save_queries()
        print(f"Added query: {keyword}")
    
    def remove_query(self, query_id: int):
        """Remove a query by ID"""
        self.queries = [q for q in self.queries if q['id'] != query_id]
        self.save_queries()
        print(f"Removed query ID: {query_id}")
    
    def toggle_query(self, query_id: int):
        """Toggle query active status"""
        for query in self.queries:
            if query['id'] == query_id:
                query['active'] = not query['active']
                self.save_queries()
                print(f"Query {query_id} {'activated' if query['active'] else 'deactivated'}")
                break
    
    def get_active_queries(self) -> List[Dict]:
        """Get all active queries"""
        return [q for q in self.queries if q['active']]
    
    def list_queries(self):
        """List all saved queries"""
        if not self.queries:
            print("No saved queries")
            return
        
        print("\nSaved Queries:")
        print("-" * 50)
        for query in self.queries:
            status = "✓" if query['active'] else "✗"
            print(f"{status} ID: {query['id']} | {query['keyword']}")
            if query['location']:
                print(f"   Location: {query['location']}")
            if query['min_price'] or query['max_price']:
                price_range = f"${query['min_price'] or 0} - ${query['max_price'] or '∞'}"
                print(f"   Price: {price_range}")
            print()

def main():
    """Interactive query manager"""
    manager = QueryManager()
    
    while True:
        print("\nQuery Manager Menu:")
        print("1. List queries")
        print("2. Add query")
        print("3. Remove query")
        print("4. Toggle query")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            manager.list_queries()
        
        elif choice == '2':
            keyword = input("Enter keyword: ").strip()
            location = input("Enter location (optional): ").strip() or None
            min_price = input("Enter min price (optional): ").strip()
            max_price = input("Enter max price (optional): ").strip()
            
            min_price = int(min_price) if min_price.isdigit() else None
            max_price = int(max_price) if max_price.isdigit() else None
            
            manager.add_query(keyword, location, min_price, max_price)
        
        elif choice == '3':
            manager.list_queries()
            query_id = input("Enter query ID to remove: ").strip()
            if query_id.isdigit():
                manager.remove_query(int(query_id))
        
        elif choice == '4':
            manager.list_queries()
            query_id = input("Enter query ID to toggle: ").strip()
            if query_id.isdigit():
                manager.toggle_query(int(query_id))
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
