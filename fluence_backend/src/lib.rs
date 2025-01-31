/*
 * Copyright 2018 Fluence Labs Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

mod error_type;
mod game_manager;
mod request_response;

use crate::error_type::AppResult;
use crate::game_manager::GameManager;
use crate::request_response::{Request, Response};

use fluence::sdk::*;
use serde_json::Value;
use std::cell::RefCell;

// use fluence::sdk::*;
use log::info;


mod settings {
    pub const DATA_MAX_COUNT: usize = 1024;
    pub const SEED: u64 = 12345678;
    // the account balance of new players
    pub const INIT_ACCOUNT_BALANCE: u64 = 100;
    // if win, player receives bet_amount * PAYOUT_RATE money
    pub const PAYOUT_RATE: u64 = 5;
}

thread_local! {
    static GAME_MANAGER: RefCell<GameManager> = RefCell::new(GameManager::new());
}

fn init() {
    logger::WasmLogger::init_with_level(log::Level::Info).unwrap();
}

fn do_request(req: String) -> AppResult<Value> {
    let request: Request = serde_json::from_str(req.as_str())?;

    match request {
        Request::AddData{
            data,
        } => GAME_MANAGER.with(|gm| gm.borrow_mut().add_data(data)),

        // Request::Roll {
        //     player_id,
        //     bet_placement,
        //     bet_size,
        // } => GAME_MANAGER.with(|gm| gm.borrow_mut().roll(player_id, bet_placement, bet_size)),

        Request::GetData { data_id } => {
            GAME_MANAGER.with(|gm| gm.borrow_mut().get_data(data_id))
        }
    }
}


#[invocation_handler]
fn main(req: String) -> String {
    match do_request(req) {
        Ok(res) => res.to_string(),
        Err(err) => {
            let response = Response::Error {
                message: err.to_string(),
            };
            serde_json::to_string(&response).unwrap()
        }
    }
}