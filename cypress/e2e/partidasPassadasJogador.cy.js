Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
        console.log(result.stdout); 
        if (result.stderr) {
            console.error(result.stderr);
        } else {
            console.log('Usuários excluídos com sucesso');
        }
    });
});


Cypress.Commands.add('deleteGerenciador', () => {
    return cy.exec('python delete_gerenciadores.py', { failOnNonZeroExit: false }).then((result) => {
        console.log(result.stdout); 
        if (result.stderr) {
            console.error(result.stderr);
        } else {
            console.log('Gerenciadores excluídos com sucesso');
        }
    });
});


Cypress.Commands.add('deleteCompeticoes', () => {
    return cy.exec('python delete_competicoes.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout);
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
});


Cypress.Commands.add('deleteTimes', () => {
    return cy.exec('python delete_times.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout);
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
});


  Cypress.Commands.add('signinGerenciador', () => {
    cy.visit('/');
    cy.get('.nav-links > :nth-child(1) > a').click();
    cy.get('#tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Gerenciador');
    cy.get('#username').type('teste gerenciador');
    cy.get('#email').type('gerenciador@email.com');
    cy.get('#password1').type('12345');
    cy.get('#password2').type('12345');
    cy.get('.btn').click();
}); 


Cypress.Commands.add('loginGerenciador', () => {
    cy.get('#username').type('teste gerenciador');
    cy.get('#password').type('12345');
    cy.get('.btn').click();
});


Cypress.Commands.add('signinJogador', () => {
    cy.visit('/');
    cy.get('.nav-links > :nth-child(1) > a').click();
    cy.get('#tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Jogador');
    cy.get('#username').type('teste jogador');
    cy.get('#email').type('jogador@email.com');
    cy.get('#password1').type('12345');
    cy.get('#password2').type('12345');
    cy.get('.btn').click();
});


Cypress.Commands.add('loginJogador', () => {
    cy.get('#username').type('teste jogador');
    cy.get('#password').type('12345');
    cy.get('.btn').click();
  });


Cypress.Commands.add('signinJogador2', () => {
    cy.visit('/');
    cy.get('.nav-links > :nth-child(1) > a').click();
    cy.get('#tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Jogador');
    cy.get('#username').type('teste jogador2');
    cy.get('#email').type('jogador2@email.com');
    cy.get('#password1').type('12345');
    cy.get('#password2').type('12345');
    cy.get('.btn').click();
});


Cypress.Commands.add('loginJogador2', () => {
    cy.get('#username').type('teste jogador2');
    cy.get('#password').type('12345');
    cy.get('.btn').click();
  });


Cypress.Commands.add('criarCompeticao', () => {
    cy.get('.card > .btn').click();
    cy.get('#nome').type('Competicao Cypress');
    cy.get('#numero_de_times').type('4');
    cy.get('#local').type('Recife');
    cy.get('button.btn').click();
});


Cypress.Commands.add('editarCompeticao', () => {
    cy.get('.card-actions > a.btn').click();
    cy.get('#nome').clear();
    cy.get('#nome').type('Edição Cypress');
    cy.get('#numero_de_times').clear();
    cy.get('#numero_de_times').type('6');
    cy.get('#local').clear();
    cy.get('#local').type('Olinda');
    cy.get('button.btn').click();

});


Cypress.Commands.add('criarTime', () => {
    cy.url().then((url) => {
      const regex = /editar(\d+)\/editar/;
      const match = url.match(regex);
  
      if (match) {
          const competicaoId = match[1];
          cy.log('ID da competição:', competicaoId);
  
          cy.get(`[href="/competicao/${competicaoId}/editar_times/"]`).click();
      } else {
          throw new Error('ID da competição não encontrado na URL!');
      }
  });
    cy.get('#nome').type('time Cypress');
    cy.get('.form-actions > .btn').click();
  });


Cypress.Commands.add('criarTime2', () => {
    cy.get('#nome').type('time Cypress2');
    cy.get('.form-actions > .btn').click();
  });
  

Cypress.Commands.add('criarPartida', () => {
    cy.url().then((url) => {
        const regex = /editar(\d+)\/editar/;
        const match = url.match(regex);
    
        if (match) {
            const competicaoId = match[1];
            cy.log('ID da competição:', competicaoId);
    
            cy.get(`[href="/competicao/${competicaoId}/partidas/"]`).click();
        } else {
            throw new Error('ID da competição não encontrado na URL!');
        }
    });
    cy.get('#time_casa');
    cy.get('select[name="time_casa"]').select('time Cypress');
    cy.get('#time_visitante');
    cy.get('select[name="time_visitante"]').select('time Cypress2');
    cy.get('#data').type('2025-04-29');
    cy.get('#hora').type('16:00');
    cy.get('form > .form-actions > .btn').click();
    cy.wait(1500);

});


Cypress.Commands.add('registrarDados', () => {
    cy.get('.btn-success').click();
    cy.get('form > :nth-child(2) > .form-control').type('3');
    cy.get('form > :nth-child(3) > .form-control').type('2');
    cy.get(':nth-child(5) > tbody > tr > :nth-child(2) > .form-control').type('3');
    cy.get(':nth-child(5) > tbody > tr > :nth-child(3) > .form-control').type('0');
    cy.get(':nth-child(5) > tbody > tr > :nth-child(4) > .form-control').type('1');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(2) > .form-control').type('2');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(3) > .form-control').type('0');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(4) > .form-control').type('0');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(5) > .form-control').type('1');
    cy.get('.btn-success').click();
});


Cypress.Commands.add('convidarJogador', () => {
    cy.get('select.form-control').eq(0).select('teste jogador');
    cy.get(':nth-child(1) > .team-players > .add-player-form > .form-group > .btn').click();
});


Cypress.Commands.add('convidarJogador2', () => {
    cy.get('select.form-control').eq(1).select('teste jogador2');
    cy.get(':nth-child(2) > .team-players > .add-player-form > .form-group > .btn').click();
});


Cypress.Commands.add('aceitarConvite', () => {
    cy.get('.btn').click();
    cy.get('form[action^="/convite/"][action$="/aceitar/"]')
    .first() 
    .then(($form) => {
        const action = $form.attr('action');
        const match = action.match(/\/convite\/(\d+)\/aceitar\//);
        const conviteId = match ? match[1] : null;

    cy.log('Convite ID encontrado:', conviteId);

    cy.wrap($form).find('.btn').click();
  });

});



describe('Visualização de Partidas passadas', () => {

    beforeEach(() => {
        cy.deleteUsers()
          .then(() => cy.deleteCompeticoes())
          .then(() => cy.deleteTimes())
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
});
    it('Cenario 1: Visualização de partidas passadas', () => {
        cy.signinJogador();
        cy.loginJogador();
        cy.get(':nth-child(3) > a').click();
        cy.signinJogador2();
        cy.loginJogador2();
        cy.get(':nth-child(3) > a').click();
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.get('.card-actions > a.btn').click();
        cy.criarTime();
        cy.criarTime2();
        cy.convidarJogador();
        cy.convidarJogador2();
        cy.get(':nth-child(3) > a').click();
        cy.loginJogador();
        cy.aceitarConvite();
        cy.get(':nth-child(3) > a').click();
        cy.loginJogador2();
        cy.aceitarConvite();
        cy.get(':nth-child(3) > a').click();
        cy.loginGerenciador();
        cy.get('.card-actions > a.btn').click();
        cy.criarPartida();
        cy.registrarDados();
        cy.get(':nth-child(3) > a').click();
        cy.loginJogador();
        cy.get(':nth-child(4) > .btn').click();
        cy.get('.btn-outline-primary').click();
        cy.wait(1000);
    });
    it('Cenario 2: Ver partida não finalizada.', () =>{
        cy.signinJogador();
        cy.loginJogador();
        cy.get(':nth-child(3) > a').click();
        cy.signinJogador2();
        cy.loginJogador2();
        cy.get(':nth-child(3) > a').click();
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.get('.card-actions > a.btn').click();
        cy.criarTime();
        cy.criarTime2();
        cy.convidarJogador();
        cy.convidarJogador2();
        cy.get(':nth-child(3) > a').click();
        cy.loginJogador();
        cy.aceitarConvite();
        cy.get(':nth-child(3) > a').click();
        cy.loginJogador2();
        cy.aceitarConvite();
        cy.get(':nth-child(3) > a').click();
        cy.loginGerenciador();
        cy.get('.card-actions > a.btn').click();
        cy.criarPartida();
        cy.get(':nth-child(3) > a').click();
        cy.loginJogador();
        cy.get(':nth-child(4) > .btn').click();
        cy.get('.btn-outline-primary').click();
        cy.wait(1000);
    });
});