describe('Client Search', () => {
    beforeEach(() => {
      cy.visit('/clients');
    });
  
    it('should search and display clients', () => {
      cy.intercept('GET', '/clients?query=Cathy', { fixture: 'clientSearch.json' }).as('searchClients');
      cy.get('input[placeholder="Search..."]').type('Cathy');
      cy.get('button[type="submit"]').click();
      cy.get('.client-card').should('have.length', 6); 
    });
  });
  